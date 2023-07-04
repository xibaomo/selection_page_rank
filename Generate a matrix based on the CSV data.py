import pandas as pd

# 根据下载完成的股票价格生成相关系数矩阵
def calculate_correlation_matrix(stock_prices):
    return stock_prices.corr()

# 创建全0的transition matrix，根据相关系数小于-0.7的条件设置元素值为1，并对每行进行归一化
def create_transition_matrix(correlation_matrix, threshold=-0.7):
    transition_matrix = pd.DataFrame(0, index=correlation_matrix.index, columns=correlation_matrix.columns)

    transition_matrix[correlation_matrix < threshold] = 1

    # 归一化每行，使每行的和等于1
    transition_matrix = transition_matrix.div(transition_matrix.sum(axis=1), axis=0)

    return transition_matrix


# 读取股票价格数据的CSV文件
csv_file_path = r'C:\Users\Administrator\Desktop\stock\stock_prices.csv'
stock_prices = pd.read_csv(csv_file_path, index_col=0)

# 生成相关系数矩阵
correlation_matrix = calculate_correlation_matrix(stock_prices)

# 创建转换矩阵
transition_matrix = create_transition_matrix(correlation_matrix)

# 打印相关系数矩阵和转换矩阵
print("相关系数矩阵:")
print(correlation_matrix)

print("转移矩阵:")
print(transition_matrix)
