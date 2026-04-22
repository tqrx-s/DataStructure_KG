import os
import time
import torch
import pandas as pd
import numpy as np
from recommend.codebase.SASRec.model import Recommendation
from recommend.codebase.SASRec.utils import *
# from model import Recommendation
# from utils import *

# 推荐知识点
def recommend_with_course(user_id):
    # 超参数设置
    dataset = 'courses2'  # 数据集名称
    train_dir = 'default'  # 训练数据目录
    batch_size = 256  # 批量大小
    maxlen = 10  # 序列的最大长度
    device = 'cpu'  # 使用的设备：'cpu' 或 'cuda'
    hidden_units = 50  # 隐藏层单元数量
    num_blocks = 1  # Transformer 中的块数量
    num_epochs = 150  # 训练的轮数
    num_heads = 1  # 多头注意力机制的头数量
    dropout_rate = 0.1  # Dropout 率
    l2_emb = 0.0  # L2 正则化系数
    lr = 0.0001  # 学习率
    cutoff = 10  # 截断长度
    choice = 0  # 是否需要重新训练模型，1 为需要

    # 数据集划分
    dataset = data_partition(dataset)
    [user_train, user_valid, user_test, usernum, itemnum] = dataset
    num_batch = len(user_train) // batch_size  # 计算批次数量
    
    # 计算平均序列长度
    cc = 0.0
    for u in user_train:
        cc += len(user_train[u])

    # 打开日志文件用于写入
    f = open(os.path.join('log.txt'), 'w')

    # 准备输出文件的列
    columns_output = ['cutoff', 'epoch', 'validation_NDCG', 'validation_hit', "test_NDCG", "test_hit"]
    res = pd.DataFrame(columns=columns_output)
    
    # 训练曲线数据框
    training_curve = pd.DataFrame(columns=['epoch', 'step', 'loss'])
    
    # 采样器
    sampler = WarpSampler(user_train, usernum, itemnum, batch_size=batch_size, maxlen=maxlen, n_workers=3)
    
    # 推荐模型实例化
    model = Recommendation(usernum, itemnum, hidden_units, num_heads, num_blocks, maxlen, dropout_rate, device).to(device)
    
    # 如果需要训练模型
    if choice == 1:
        for cutoff in [5, 10, 15]:  # 不同的截断长度进行训练和评估
            print("cutoff:", cutoff)
            sampler = WarpSampler(user_train, usernum, itemnum, batch_size=batch_size, maxlen=maxlen, n_workers=3)
            model = Recommendation(usernum, itemnum, hidden_units, num_heads, num_blocks, maxlen, dropout_rate, device).to(device)
            
            # 参数初始化
            for name, param in model.named_parameters():
                try:
                    torch.nn.init.xavier_uniform_(param.data)
                    print('success', name)
                except:
                    print('failed init layer', name)
                    pass  # 忽略初始化失败的层
            
            model.train()  # 启用模型训练模式
            epoch_start_idx = 1
            bce_criterion = torch.nn.BCEWithLogitsLoss()  # 损失函数
            adam_optimizer = torch.optim.Adam(model.parameters(), lr=lr, betas=(0.9, 0.98))  # 优化器
            
            T = 0.0
            t0 = time.time()
            
            print('Working on the parameter num_heads: ', num_heads)
            for epoch in range(epoch_start_idx, num_epochs + 1):
                for step in range(num_batch):
                    # seq：用户的历史交互序列
                    # pos：正样本序列，表示用户在 seq 中下一个真正与之交互的物品ID。
                    # neg：负样本序列，表示用户没有与之交互的物品ID，用于对比学习。
                    u, seq, pos, neg = sampler.next_batch()  # 获取一个批次的数据
                    u, seq, pos, neg = np.array(u), np.array(seq), np.array(pos), np.array(neg)
                    
                    # 前向传播
                    # pos_logits 和 neg_logits 是模型对正样本和负样本的预测分数
                    # pos_logits 表示用户可能会与这些物品交互的程度 
                    # neg_logits 表示用户不太可能与这些物品交互的程度
                    pos_logits, neg_logits = model(seq, pos, neg)   #调用forward方法
                    # pos_labels：一个全为1的张量 neg_labels：一个全为0的张量
                    # 二者表示pos_logits, neg_logits应该得到的分数，用于计算损失
                    pos_labels, neg_labels = torch.ones(pos_logits.shape, device=device), torch.zeros(neg_logits.shape, device=device)
                    
                    adam_optimizer.zero_grad()  # 梯度清零
                    indices = np.where(pos != 0)    #找到在数组 pos 中非零元素的索引，即用户点击过的课程索引
                    loss = bce_criterion(pos_logits[indices], pos_labels[indices])  #计算正样本的二叉熵损失
                    loss = loss.clone() + bce_criterion(neg_logits[indices], neg_labels[indices])   #计算负样本的二叉熵损失
                    # 添加L2正则化项到损失函数，防止过拟合
                    for param in model.item_embedding.parameters():
                        loss = loss.clone() + l2_emb * torch.norm(param)
                    
                    loss.backward()  # 反向传播
                    adam_optimizer.step()  # 优化器更新
                    
                    if step % 10 == 0:
                        print("loss in epoch {} iteration {}: {}".format(epoch, step, loss.item()))  # 打印损失值
                    
                    # 将每个epoch中最后一个step的损失值记录下来，并将其添加到训练曲线
                    if step == num_batch - 1:
                        To_output = [[epoch, step, loss.item()]]
                        training_curve = training_curve.append(pd.DataFrame(To_output, columns=['epoch', 'step', 'loss']))
                
                if epoch % 5 == 0 or epoch == num_epochs:
                    model.eval()  # 评估模式
                    t1 = time.time() - t0
                    T += t1
                    print('Evaluating', end='')
                    
                    # 评估模型
                    t_test = evaluate(model, dataset, maxlen, cutoff)
                    t_valid = evaluate_valid(model, dataset, maxlen, cutoff)
                    print('\n epoch:%d, time: %f(s), valid (NDCG@10: %.4f, HR@10: %.4f), test (NDCG@10: %.4f, HR@10: %.4f)'
                            % (epoch, T, t_valid[0], t_valid[1], t_test[0], t_test[1]))
                    
                    f.write(str(t_valid) + ' ' + str(t_test) + '\n')
                    f.flush()
                    t0 = time.time()
                    model.train()  # 重新进入训练模式
                    
                    if epoch == num_epochs:
                        To_output = [[cutoff, epoch, t_valid[0], t_valid[1], t_test[0], t_test[1]]]
                        res = res.append(pd.DataFrame(To_output, columns=columns_output))
            
                if epoch == num_epochs:
                    fname = 'model_param.pth'
                    torch.save(model.state_dict(), os.path.join(fname))  # 保存模型参数
    
    # 加载预训练模型参数
    model.load_state_dict(torch.load(r'D:\Program Files (x86)\study\graduation Project\DataStructure_KG-master\recommend\codebase\SASRec\model_param.pth'))
    f.close()
    sampler.close()
    
    res.to_csv("Experiment with cutoff.csv")  # 保存实验结果
    # training_curve.to_csv("training_curve(200epochs).csv")

    # 输出推荐结果
    output_hit10(model, dataset, maxlen, user_id)
    
    # 读取推荐结果和课程名称
    course_index = pd.read_csv(r"D:\Program Files (x86)\study\graduation Project\DataStructure_KG-master\recommend\codebase\SASRec\result_hit10_user.csv")
    course_names = pd.read_csv(r"D:\Program Files (x86)\study\graduation Project\DataStructure_KG-master\recommend\codebase\SASRec\data\name.csv")
    
    # 合并数据并保存
    data = pd.merge(course_index, course_names, on='course_index')
    data.to_csv(r'D:\Program Files (x86)\study\graduation Project\DataStructure_KG-master\recommend\codebase\SASRec\recommend.csv', index=False)
    
    # 读取推荐结果并返回前 10 个推荐的课程名称
    file = open(r"D:\Program Files (x86)\study\graduation Project\DataStructure_KG-master\recommend\codebase\SASRec\recommend.csv", 'r', encoding='UTF-8')
    ans = []
    for line in file.readlines()[1:11]:
        line = line.strip().split(',')
        ans.append(line[2])
    file.close()
    print(ans)
    
    return ans


def recommend_new_user(new_course):
    # 数据集文件路径
    dataset_path = r'D:\Program Files (x86)\study\graduation Project\DataStructure_KG-master\recommend\codebase\SASRec\data\courses2.txt'
    
    # 读取现有数据集
    with open(dataset_path, 'r') as file:
        lines = file.readlines()
    
    # 找到当前最大用户ID
    max_user_id = 0
    for line in lines:
        user_id, _ = map(int, line.split())
        if user_id > max_user_id:
            max_user_id = user_id
    
    # 新用户ID为当前最大用户ID加1
    new_user_id = max_user_id + 1
    
    # 创建新用户的数据
    new_user_data = [f"{new_user_id} {course_id}\n" for course_id in new_course]
    
    # 将新用户的数据添加到现有的数据集中
    with open(dataset_path, 'a') as file:
        file.writelines(new_user_data)
    
    # print(f"新用户ID为: {new_user_id}")

    return(recommend_with_course(new_user_id))

if __name__ == '__main__':
    # recommend_with_course(0)
    new_courses = [44, 25, 67]  
    recommend_new_user(new_courses)

    