import csv

# 定义文件路径
file_path = "C:/info.csv"

# 读取 CSV 文件
try:
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # 读取并打印每一行
        for row in csv_reader:
            print(row)
except FileNotFoundError:
    print(f"文件未找到: {file_path}")
except Exception as e:
    print(f"发生错误: {e}")