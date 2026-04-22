import sys
import copy
import torch
import random
import numpy as np
import pandas as pd
from collections import defaultdict
from multiprocessing import Process, Queue

# 随机生成不在集合s中的整数，范围在[l, r)之间
def random_neq(l, r, s):
    t = np.random.randint(l, r)
    while t in s:
        t = np.random.randint(l, r)
    return t

# 样本生成函数，用于多进程并行采样
def sample_function(user_train, usernum, itemnum, batch_size, maxlen, result_queue, SEED):
    def sample():
        # 随机选择一个有足够交互记录的用户
        user = np.random.randint(0, usernum)
        while len(user_train[user]) <= 1: 
            user = np.random.randint(1, usernum + 1)

        # 初始化序列和正负样本
        seq = np.zeros([maxlen], dtype=np.int32)
        pos = np.zeros([maxlen], dtype=np.int32)
        neg = np.zeros([maxlen], dtype=np.int32)
        nxt = user_train[user][-1]
        idx = maxlen - 1

        # 记录用户的历史交互物品
        ts = set(user_train[user])
        for i in reversed(user_train[user][:-1]):
            seq[idx] = i
            pos[idx] = nxt
            if nxt != 0: 
                neg[idx] = random_neq(1, itemnum + 1, ts)
            nxt = i
            idx -= 1
            if idx == -1: 
                break

        return (user, seq, pos, neg)

    np.random.seed(SEED)
    while True:
        one_batch = [sample() for _ in range(batch_size)]
        result_queue.put(zip(*one_batch))

# WarpSampler类用于多进程生成批次样本
class WarpSampler(object):
    def __init__(self, User, usernum, itemnum, batch_size=64, maxlen=10, n_workers=1):
        self.result_queue = Queue(maxsize=n_workers * 10)
        self.processors = [
            Process(
                target=sample_function, 
                args=(User, usernum, itemnum, batch_size, maxlen, self.result_queue, np.random.randint(2e9))
            ) for _ in range(n_workers)
        ]
        for p in self.processors:
            p.daemon = True
            p.start()

    # 获取下一个批次
    def next_batch(self):
        return self.result_queue.get()

    # 关闭所有进程
    def close(self):
        for p in self.processors:
            p.terminate()
            p.join()

# 数据分割函数
def data_partition(fname):
    usernum = 0
    itemnum = 0
    User = defaultdict(list)
    user_train = {}
    user_valid = {}
    user_test = {}
    
    # 读取用户-物品交互数据
    with open(f'D:/Program Files (x86)/study/graduation Project/DataStructure_KG-master/recommend/codebase/SASRec/data/{fname}.txt', 'r', encoding="utf-8") as f:
        for line in f:
            u, i = map(int, line.rstrip().split(' '))
            usernum = max(u, usernum)
            itemnum = max(i, itemnum)
            User[u].append(i)

    # 划分训练集、验证集和测试集
    for user in User:
        nfeedback = len(User[user])
        if nfeedback < 3:
            user_train[user] = User[user]
            user_valid[user] = []
            user_test[user] = []
        else:
            user_train[user] = User[user][:-2]
            user_valid[user] = [User[user][-2]]
            user_test[user] = [User[user][-1]]
    
    return [user_train, user_valid, user_test, usernum, itemnum]

# 评估模型在测试集上的表现
def evaluate(model, dataset, maxlen, cutoff):
    [train, valid, test, usernum, itemnum] = copy.deepcopy(dataset)

    NDCG = 0.0
    HT = 0.0
    valid_user = 0.0

    # 选择最多10000个用户进行评估
    users = random.sample(range(0, usernum + 1), 10000) if usernum > 10000 else range(0, usernum)
    
    for u in users:
        if len(train[u]) < 1 or len(test[u]) < 1: 
            continue

        # 构建用户的序列输入
        seq = np.zeros([maxlen], dtype=np.int32)
        idx = maxlen - 1
        seq[idx] = valid[u][0]
        idx -= 1
        
        for i in reversed(train[u]):
            seq[idx] = i
            idx -= 1
            if idx == -1: 
                break
        
        rated = set(train[u])
        rated.add(0)
        item_idx = [test[u][0]]
        not_chosen = set(range(1, itemnum + 1)) - set(item_idx) - rated
        item_idx.extend(list(not_chosen))

        # 预测评分
        predictions = -model.predict(*[np.array(l) for l in [[seq], item_idx]])
        predictions = predictions[0]

        rank = predictions.argsort().argsort()[0].item()
        valid_user += 1

        # 计算NDCG和命中率
        if rank < cutoff:
            NDCG += 1 / np.log2(rank + 2) if rank > 0 else 1
            HT += 1
        
        if valid_user % 100 == 0:
            sys.stdout.flush()

    return NDCG / valid_user, HT / valid_user

# 在验证集上评估模型表现
def evaluate_valid(model, dataset, maxlen, cutoff):
    [train, valid, test, usernum, itemnum] = copy.deepcopy(dataset)

    NDCG = 0.0
    valid_user = 0.0
    HT = 0.0
    
    users = random.sample(range(0, usernum + 1), 10000) if usernum > 10000 else range(0, usernum + 1)
        
    for u in users:
        if len(train[u]) < 1 or len(valid[u]) < 1: 
            continue

        # 构建用户的序列输入
        seq = np.zeros([maxlen], dtype=np.int32)
        idx = maxlen - 1
        
        for i in reversed(train[u]):
            seq[idx] = i
            idx -= 1
            if idx == -1: 
                break

        rated = set(train[u])
        rated.add(0)
        item_idx = [valid[u][0]]
        not_chosen = set(range(1, itemnum + 1)) - set(item_idx) - rated
        item_idx.extend(list(not_chosen))

        # 预测评分
        predictions = -model.predict(*[np.array(l) for l in [[seq], item_idx]])
        predictions = predictions[0]

        rank = predictions.argsort().argsort()[0].item()
        valid_user += 1

        # 计算NDCG和命中率
        if rank < cutoff:
            NDCG += 1 / np.log2(rank + 2) if rank > 0 else 1
            HT += 1
        
        if valid_user % 100 == 0:
            sys.stdout.flush()

    return NDCG / valid_user, HT / valid_user

# 输出命中率@10的结果
def output_hit10(model, dataset, maxlen, user_id):
    res = pd.DataFrame(columns=['userid', 'course_index'])
    [train, valid, test, usernum, itemnum] = copy.deepcopy(dataset)
    
    if user_id in test:
        # 构建用户的序列输入
        seq = np.zeros([maxlen], dtype=np.int32)
        idx = maxlen - 1
        
        for i in reversed(train[user_id]):
            seq[idx] = i
            idx -= 1
            if idx == -1: 
                break

        rated = set(train[user_id])
        rated.add(0)
        item_idx = [valid[user_id][0]]
        not_chosen = set(range(1, itemnum + 1)) - set(item_idx) - rated
        item_idx.extend(list(not_chosen))

        # 预测评分
        predictions = -model.predict(*[np.array(l) for l in [[seq], item_idx]])
        predictions = predictions[0]
        rank = predictions.argsort()[:10] + 1
        
        # 保存结果
        temp = [[user_id, i] for i in rank.cpu().detach().numpy()]
        res = res.append(pd.DataFrame(temp, columns=['userid', 'course_index']))
    
    res.to_csv("result_hit10_user.csv", index=False)
