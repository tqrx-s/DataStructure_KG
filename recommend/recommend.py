import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import math
from math import *
import sys
sys.path.append("..")

# 读取data.csv中每行中除了名字的数据
file = open(r"D:\Program Files (x86)\study\graduation Project\DataStructure_KG-master\recommend\data2.csv", 'r', encoding='UTF-8')
data = {}  # 只存放每位用户评论的知识点和评分
for line in file.readlines()[1:23736]: # 数据集的data总共23736行
    # 注意这里不是readline()
    line = line.strip().split(',')
    # 如果字典中没有某位用户，则使用用户ID来创建这位用户
    if not line[0] in data.keys():
        data[line[0]] = {line[3]: line[1]}
    # 否则直接添加以该用户ID为key字典中
    else:
        data[line[0]][line[3]] = line[1]
file.close()

#余弦相似度
def cosine(user1, user2):
    # 取出两位用户评论过的知识点和评分
    user1_data = data[user1]
    user2_data = data[user2]
    common = {}

    # 找到两位用户都评论过的知识点
    for key in user1_data.keys():
        if key in user2_data.keys():
            common[key] = 1
    if len(common) == 0:
        return 0  # 如果没有共同评论过的知识点，则返回0
    n = len(common)  # 共同知识点数目
    # print(n,common)

    # 计算评分和
    sum1 = sum([float(user1_data[knowledge]) for knowledge in common])
    sum2 = sum([float(user2_data[knowledge]) for knowledge in common])

    # 计算评分平方和
    sum1Sq = sum([pow(float(user1_data[knowledge]), 2) for knowledge in user1_data])
    sum2Sq = sum([pow(float(user2_data[knowledge]), 2) for knowledge in user2_data])

    # 计算乘积和
    PSum = sum([float(user1_data[it])*float(user2_data[it]) for it in common])

    # 计算相关系数
    den = sqrt((sum1Sq)*(sum2Sq))
    if den == 0:
        return 0
    result = PSum/den
    return result

#皮尔逊相关系数
def pearson_sim_pro(user1, user2):
    # 取出两位用户评论过的知识点和评分
    user1_data = data[user1]
    user2_data = data[user2]
    common = {} # 以字典形式包括目标用户和参考用户共同看过的知识点

    # 找到两位用户都评论过的知识点
    for key in user1_data.keys():
        if key in user2_data.keys():
            common[key] = 1
    if len(common) == 0:
        return 0  # 如果没有共同评论过的知识点，则返回0
    n = len(common) 
    
    # 计算分子,235是知识点数目
    sum_of_product_of_xy = 235 * sum(float(user1_data[knowledge]) * float(user2_data[knowledge]) for knowledge in common)
    product_of_sum_of_x_and_y = sum(float(user1_data[knowledge]) for knowledge in common) * sum(float(user2_data[knowledge]) for knowledge in common)
    num = sum_of_product_of_xy - product_of_sum_of_x_and_y
    

    # 计算分母参数以及分母
    sum1 = pow(sum([float(user1_data[knowledge]) for knowledge in user1_data]), 2)
    sum2 = pow(sum([float(user2_data[knowledge]) for knowledge in user2_data]), 2)
    sum1Sq = 235 * sum([pow(float(user1_data[knowledge]), 2) for knowledge in user1_data])
    sum2Sq = 235 * sum([pow(float(user2_data[knowledge]), 2) for knowledge in user2_data])
    den1 = sum1Sq - sum1
    den2 = sum2Sq - sum2
    den = sqrt(den1 * den2)

    if den == 0:
        return 0
    r = num / den
    return r


# 计算某个用户与其他用户的相似度
def top_simliar(userID, choice):
    # 空列表，有东西再往进加
    res = []
    for userid in data.keys(): #这里要做循环，把目标用户与所有其他用户的相似度都计算出来再排序
        # 排除与自己计算相似度
        if not userid == userID:
            #选择相似度计算方法
            if(choice == '1'):
                simliar = cosine(userID, userid)
            else:
                simliar = pearson_sim_pro(userID, userid)
            res.append((userid, simliar))
    res.sort(key = lambda val: val[1])
    res.reverse()
    return res

# 均方根误差
def RMSE(records):
    count = 0
    allsum = 0
    while count < len(records):
        allsum += pow(records[count][1] - float(records[count][0]), 2)
        count += 1
    avg = allsum / float(len(records))
    return math.sqrt(avg)   

# 平均绝对误差
def MAE(records):
    count = 0
    allsum = 0
    while count < len(records):
        allsum += abs(records[count][1] - float(records[count][0]))
        count += 1
    avg = allsum  / float(len(records))
    return math.sqrt(avg) 

def recommend_with_predict(user, num_of_user):
    # 相似度最高的用户
    # print("1.cosine\n2.preason_sim")
    # choice = input("用哪个方法？")
    # 打印相关度最高的前十个用户
    user = str(user)
    RES = top_simliar(user, 2)
    # print("相关度最高的前二十名用户：", RES)
    
    # 得到用户名和相似值，为下一步计算做准备
    top_sim_user_data = [] # 存放最相似用户看过的知识点和相应的评分
    weight = [] # 存放最相似用户的相似度
   
    count = 0
    while count < num_of_user:
        top_sim_user_data.append(data[RES[count][0]])
        weight.append(float(RES[count][1]))
        # print("最相似用户", count + 1, "的名字和相似度：", RES[count][0], RES[count][1], "\n")        
        count += 1
        
    user_data = data[user]
    # 计算评分平均数
    ave = []
    count = 0
    while count < num_of_user:
        ave.append(sum(float(top_sim_user_data[count][knowledge]) for knowledge in top_sim_user_data[count].keys()) / len(top_sim_user_data[count]))
        count += 1

    # 被推荐人的平均分
    ave_predicted = sum(float(user_data[knowledge]) for knowledge in user_data.keys()) / len(user_data) 
    
    # 读取知识点名字
    file = open(r"D:\Program Files (x86)\study\graduation Project\DataStructure_KG-master\recommend\data2.csv", 'r', encoding = 'UTF-8')
    knowledge2 = []
    for line in file.readlines()[1:236]:
        line = line.strip().split(',')
        knowledge2.append(line[3])
    file.close()
    
    knowledge2 = sorted(knowledge2)

    # 用一个字典存储各个用户的知识点及其分数，如果没有看过，则分数为0
    user_scores = {}
    count = 0
    while count < num_of_user:
        user_scores[count] = {}
        # 模仿之前的data导入
        for knowledge in knowledge2:            
            if knowledge not in top_sim_user_data[count].keys():
                user_scores[count][knowledge] =  0.0
            else:
                user_scores[count][knowledge] = float(top_sim_user_data[count][knowledge])
        count += 1

    predict_knowledge2 = []
    # 做出预测
    sensitivety = 1.0
    epsilon = 1
   
# choice_of_laplace = input("要不要加差分隐私？\n“y”代表确认")
    choice_of_laplace = 1
    if  choice_of_laplace != 0:
        # sensitivety = float(input("输入敏感度："))
        # epsilon = float(input("输入差分隐私参数："))              
        beta = sensitivety / epsilon

    
    # 根据前几名最相似的用户，将他们对各自知识点的评分乘以权重，得到预测分数
    for knowledge in knowledge2:
        count = 0
        sum_of_weight = 0 # 权重求和
        predict_score = 0
        while count < num_of_user:
            # 评分为0，即该用户没有看过这个知识点
            if user_scores[count][knowledge] == 0.0: 
                weight_temp =  0.0 # weight_temp是循环到每个用户的权重值，算加权总分的时候可以用
            else:
                weight_temp = weight[count]
                predict_score += float(user_scores[count][knowledge] - ave[count]) * weight_temp
            sum_of_weight += weight_temp           
            count += 1

        # 若权重和不为0则计算原始预测值，反之，原始预测值为被推荐用户对其所有观看知识点的平均分
        if sum_of_weight != 0: 
            predict_score = predict_score / sum_of_weight + ave_predicted
        else:
            predict_score = ave_predicted

        # 判断要不要加拉普拉斯噪声
        if  choice_of_laplace != 0: 
            predict_score += np.random.laplace(0, beta, 1)

        predict_knowledge2.append((knowledge, float(predict_score)))
    
    # 去重
    predict_knowledge2 = list(set(predict_knowledge2))

    # 删除用户自己看过的知识点，顺便计算均方根误差和平均绝对误差
    predicted_user = []
    count = 0
    while count < len(predict_knowledge2):
        if predict_knowledge2[count][0] in user_data.keys():
            predicted_user.append((user_data[predict_knowledge2[count][0]], predict_knowledge2[count][1])) #把实际分数和预测分数放在这个新列表里
            del predict_knowledge2[count]
        count += 1
    
    value_of_rmse =  RMSE(predicted_user)
    value_of_mae = MAE(predicted_user)
    print(user, "在推荐人数为", num_of_user, "的均方根误差为：", value_of_rmse, "平均绝对误差为：", value_of_mae)
    return value_of_rmse, value_of_mae

#推荐知识点
def recommend_with_knowledge(userID):
    ans = []
    user = str(userID)
    RES = top_simliar(user, 2)
    top_sim_user_id = RES[0][0] # 存放最相似用户的id
    print("最相似用户的ID和相似度：", RES[0][0], RES[0][1])        
    # print("对应行数：",235 * (int(top_sim_user_id)-1) + 2,235 * int(top_sim_user_id) + 1)
    file = open(r"D:\Program Files (x86)\study\graduation Project\DataStructure_KG-master\recommend\data2.csv", 'r', encoding='UTF-8')
    for line in file.readlines()[235 * (int(top_sim_user_id)-1) + 2:235 * int(top_sim_user_id) + 1]: # 最相似用户的信息所在行
        line = line.strip().split(',')
        if line[1] == str(5.0):
            ans.append(line[3])
    file.close()
    # print("推荐知识点：",ans)
    return ans

# if __name__ == '__main__':
#     users = []
#     count = 1
#     while count < 6:
#         users.append(str(count))
#         count += 1

#     num_list = []
#     count = 40
#     while count <= 100:
#         num_list.append(count)  
#         count += 10
    
#     RMSE_list = []
#     MAE_list = []
#     writer_of_RMSE = pd.ExcelWriter(r"D:\Program Files (x86)\study\graduation Project\DataStructure_KG-master\recommend\xls\RMSE.xlsx")
#     writer_of_MAE = pd.ExcelWriter(r"D:\Program Files (x86)\study\graduation Project\DataStructure_KG-master\recommend\xls\MAE.xlsx")

#     # writer_of_RMSE = pd.ExcelWriter("/home/jerryw/Desktop/graduate/xls/RMSE.xlsx")
#     # writer_of_MAE = pd.ExcelWriter("/home/jerryw/Desktop/graduate/xls/MAE.xlsx")
    
#     for user in users: 
#         value_of_RMSE = []
#         value_of_MAE = []
#         for number in num_list:
#             Recommendations = recommend_with_predict(user, number)
#             value_of_RMSE.append(Recommendations[0])
#             value_of_MAE.append(Recommendations[1])
#         RMSE_list.append(value_of_RMSE)
#         MAE_list.append(value_of_MAE)

#     table_of_RMSE = pd.DataFrame(RMSE_list, index = users, columns = num_list)
#     print("不同用户在参考用户数量不同时得到的RMSE如下\n", table_of_RMSE)
#     table_of_MAE = pd.DataFrame(MAE_list, index = users, columns = num_list)
#     print("不同用户在参考用户数量不同时得到的MAE如下\n", table_of_MAE)
#     table_of_RMSE.to_excel(writer_of_RMSE)
#     table_of_MAE.to_excel(writer_of_MAE)
#     writer_of_RMSE._save()
#     writer_of_MAE._save()

#     recommend_with_knowledge(1)