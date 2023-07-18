import yfinance as yf
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt

def calculate_correlation_matrix(stock_list_file, start_date, end_date):
    # 下载多个股票的数据
    sp500 = pd.read_csv(stock_list_file)
    tickers = sp500['Symbol'].tolist()
    data = yf.download(tickers, start=start_date, end=end_date, interval="1d")

    # 从下载的数据中提取收盘价，并创建价格矩阵
    price_matrix = data['Close']

    # 剔除生成股票价格少于10的股票
    price_matrix = price_matrix.dropna(thresh=10, axis=1)

    # 生成股票价格相关系数矩阵
    corr_matrix = price_matrix.corr()

    # 对相关系数矩阵进行处理
    for row in corr_matrix.index:
        negatives = corr_matrix.loc[row, corr_matrix.loc[row] < 0]
        negatives_sum = negatives.sum()
        corr_matrix.loc[row, corr_matrix.loc[row] >= 0] = 0
        corr_matrix.loc[row, corr_matrix.loc[row] < 0] = corr_matrix.loc[row, corr_matrix.loc[row] < 0] / negatives_sum
    # 将对角线上的值设为零
    corr_matrix.values[range(len(corr_matrix)), range(len(corr_matrix))] = 0
    # 删除全为零的行
    corr_matrix = corr_matrix.loc[(corr_matrix != 0).any(axis=1)]
    # 打印处理后的相关系数矩阵
    # print("Processed correlation matrix：")
    # print(corr_matrix)
    return corr_matrix

def compute_stationary_distribution(trans_mat):
    nd = trans_mat.shape[0]
    row_one = np.ones((1,nd))
    I = np.eye(nd)
    ONE = np.ones((nd,nd))
    tmp = I - trans_mat + ONE
    tmp = np.linalg.inv(tmp)
    v = row_one @ tmp
    return v[0,:]
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: {} <stock_list_file> <start_date> <end_date>".format(sys.argv[0]))
        sys.exit(1)

    stock_list_file = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    
    trans_matrix = calculate_correlation_matrix(stock_list_file, start_date, end_date)
    v = compute_stationary_distribution(trans_matrix.values)
    syms = trans_matrix.index.values

    sort_id = np.argsort(v)[::-1]

    score = v[sort_id][:10]
    syms  = syms[sort_id][:10]

    plt.stem(syms,score)
    plt.show()
