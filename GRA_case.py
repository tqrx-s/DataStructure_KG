import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#无量纲化
def dimensionlessProcessing(df):
    newDataFrame = pd.DataFrame(index=df.index)
    columns = df.columns.tolist()
    for c in columns:
        d = df[c]
        MAX = d.max()
        MIN = d.min()
        MEAN = d.mean()
        # newDataFrame[c] = ((d - MEAN) / (MAX - MIN)).tolist()
        newDataFrame[c] = ((d - MIN) / (MAX - MIN)).tolist()
    return newDataFrame

def GRA_ONE_NEWCASE(new_case, history_data):
    # 对历史数据和新案例进行无量纲化处理
    history_data_dimless = dimensionlessProcessing(history_data)
    new_case = pd.Series(new_case, index=history_data.columns)
    new_case = (new_case - new_case.mean()) / (new_case.max() - new_case.min())

    # 计算差值矩阵
    shape_n, shape_m = history_data_dimless.shape[0], history_data_dimless.shape[1]
    a = np.zeros([shape_n, shape_m])
    for i in range(shape_n):
        for j in range(shape_m):
            a[i, j] = abs(history_data_dimless.iloc[i, j] - new_case[j])

    # 取出差值矩阵中的最大值和最小值
    c, d = np.amax(a), np.amin(a)

    # 计算灰色关联系数矩阵
    result = np.zeros([shape_n, shape_m])
    for i in range(shape_n):
        for j in range(shape_m):
            result[i, j] = (d + 0.5 * c) / (a[i, j] + 0.5 * c)

    # 计算每个历史案例的灰色关联度（均值）
    gra_values = [np.mean(result[i, :]) for i in range(shape_n)]

    # 将灰色关联值与原始数据合并
    gra_df = pd.DataFrame({
        "GRA Value": gra_values,
        **{col: history_data[col] for col in history_data.columns}
    })

    return gra_df



# 找到与新案例最相似的前十个历史案例
def find_top_similar_cases(new_case, history_data):
    gra_df = GRA_ONE_NEWCASE(new_case, history_data)
    # 按 "GRA Value" 列排序，并选择前十行
    top_similar_cases = gra_df.nlargest(10, "GRA Value")
    return top_similar_cases



if __name__ == "__main__":
    wine = pd.read_csv("wine.csv",index_col=0)
    lesson = pd.read_csv("lesson.csv")

# lesson参数分别为：
# 序号
# 星期（1-7）
# 时间（小时+分钟，如13点30分表示为1330）
# 学科（1-14，1哲学，2经济学，3法学，4教育学，5文学，6历史学，7理学，8工学，9农学，10医学，11军事学，12管理学，13艺术学，14交叉学）
# 地点（1-6，1三教，2四教，3东教，4五教，5实验楼，6其他）
# 学生高频行为1（1-8，认真听讲1，看手机2，趴桌子3，交头接耳4，低头5，站立6，举手7，挠头8）
# 学生高频行为2（1-8，认真听讲1，看手机2，趴桌子3，交头接耳4，低头5，站立6，举手7，挠头8）
# 教师高频行为（1-9，提问同学1，双手比划2，写板书3，来回走动4，授课5，课件展示6，引导讨论7，巡视教室8，观察学生9）
# 抬头率(抬头学生占总学生的比率，可以取不同时间的抬头率平均得到)
# 师生交互次数
# 写板书时间
# 课堂测验分数（课下作业分数也行）


    # wine_case = [0, 7.5, 0.55, 0.2, 2.5, 0.075, 12, 30, 0.997, 3.4, 0.65, 10, 5] 
    wine_case_itself = [7.4, 0.59, 0.08, 4.4, 0.086, 6,29, 0.9974, 3.38, 0.5, 9, 4] 
    # lesson_case = [0, 1, 1005, 8, 3, 5, 1, 1, 0.1, 4, 45, 80]

    top_similar_cases = find_top_similar_cases(wine_case_itself, wine)
    # top_similar_cases = find_top_similar_cases(wine_case, wine)
    # top_similar_cases = find_top_similar_cases(lesson_case, lesson)
    print(f"最相似的前十个历史案例：\n{top_similar_cases}")



