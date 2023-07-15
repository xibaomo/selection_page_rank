import yfinance as yf
import pandas as pd

# 下载多个股票的数据
sp500 = pd.read_csv(r'C:\Users\Administrator\Desktop\sock\constituents_csv.csv')
tickers = sp500['Symbol'].tolist()
data = yf.download(tickers, start="2023-01-01", end="2023-06-30", interval="1d")

# 从下载的数据中提取收盘价，并创建价格矩阵
price_matrix = data['Close']

# 剔除生成股票价格少于10的股票
price_matrix = price_matrix.dropna(thresh=10, axis=1)
# 打印价格矩阵
print("Price Matrix:")
print(price_matrix)
# 生成股票价格相关系数矩阵
corr_matrix = price_matrix.corr()

# 对相关系数矩阵进行处理
for column in corr_matrix.columns:
    negatives = corr_matrix[corr_matrix[column] < 0][column]
    negatives_sum = negatives.sum()
    corr_matrix.loc[corr_matrix[column] >= 0, column] = 0
    corr_matrix.loc[corr_matrix[column] < 0, column] = corr_matrix.loc[corr_matrix[column] < 0, column] / negatives_sum

# 打印处理后的相关系数矩阵
print("Processed Correlation Matrix:")
print(corr_matrix)
