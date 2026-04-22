import pandas as pd

# 读取 data3.csv 文件
data = pd.read_csv("data3.csv")

# 过滤出类型为计算机的条目
filtered_data = data[data['type'] == '计算机']

# 创建一个字典，将原始的 stu_id 映射到新的连续编号
id_mapping = {old_id: new_id for new_id, old_id in enumerate(filtered_data['stu_id'].unique(), start=1)}

# 使用字典将原始的 stu_id 映射到新的连续编号
filtered_data['stu_id'] = filtered_data['stu_id'].map(id_mapping)

# 创建一个字典，将原始的 course_index 映射到新的连续编号
index_mapping = {old_index: new_index for new_index, old_index in enumerate(filtered_data['course_index'].unique(), start=1)}

# 使用字典将原始的 course_index 映射到新的连续编号
filtered_data['course_index'] = filtered_data['course_index'].map(index_mapping)

# 删除类型和类型ID属性
filtered_data = filtered_data.drop(columns=['type', 'type_id'])

# 将处理后的数据保存到新的 CSV 文件
filtered_data.to_csv("filtered_data.csv", index=False)

print("处理完成，已将重新编号后的数据保存到 filtered_data.csv 文件中。")
