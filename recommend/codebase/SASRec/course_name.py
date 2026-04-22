import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from math import *
import random


# 读取知识点名字
file = open(r"D:\Program Files (x86)\study\graduation Project\Course-Recommendation-for-MOOCs-main\codebase\data\course2.csv", 'r', encoding = 'UTF-8')
names = []
for line in file.readlines()[1:1303]:
    line = line.strip().split(',')
    names.append(line[1])
file.close()

filename='data2.csv'
#根据需求调整k的序号
k = 100
# 输出生成的随机数
for _ in range(1000):    
    cnt = 0
    # 生成235个随机数，范围在0到5之间
    random_numbers = [random.randint(0, 10)/2 for _ in range(235)]
    #随机的rating总和在625到825间
    total_sum = sum(random_numbers)
    if total_sum >=625 and total_sum<=825:
        k += 1
        if k > 101:
            break
        else:
            for i,j in zip(random_numbers,names):
                cnt += 1
                msg=f'{k},{i},{cnt},{j}'
                # print(msg)
                with open(filename,'a',encoding="UTF-8")as f:
                    f.write(msg + "\n")
                    f.close
