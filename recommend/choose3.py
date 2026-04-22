import pandas as pd

# 读取 data3.csv 文件
data = pd.read_csv("data.csv")

# 删除类型和类型ID属性
filtered_data = data.drop(columns=['userId', 'rating', 'knowledgeId'])

# 将处理后的数据保存到新的 CSV 文件
filtered_data.to_csv("filtered_data5.csv", index=False)

print("处理完成，已将重新编号后的数据保存到 filtered_data5.csv 文件中。")
