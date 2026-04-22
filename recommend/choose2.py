import pandas as pd

# 读取 filtered_data.csv 文件
data = pd.read_csv("filtered_data.csv")

# 创建一个字典，将原始的 course_index 映射到新的连续编号
index_mapping = {old_index: new_index for new_index, old_index in enumerate(data['course_index'].unique(), start=1)}

# 使用字典将原始的 course_index 映射到新的连续编号
data['course_index'] = data['course_index'].map(index_mapping)

# 删除属性
filtered_data = data.drop(columns=['time','name'])

#去重
filtered_data = filtered_data.drop_duplicates()

filtered_data['stu_id'] = filtered_data['stu_id'] - 1

# 将处理后的数据保存到新的 CSV 文件
filtered_data.to_csv("filtered_data4.csv", index=False)

print("处理完成，已将重新编号后的数据保存到 filtered_data4.csv 文件中。")
