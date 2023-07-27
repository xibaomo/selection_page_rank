import yfinance as yf
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt

def calculate_correlation_matrix(price_matrix):
   
    corr_matrix = price_matrix.corr()

    # 对相关系数矩阵进行处理
    for row in corr_matrix.index:
        negatives = corr_matrix.loc[row, corr_matrix.loc[row] < 0]
        negatives_sum = negatives.sum()
        corr_matrix.loc[row, corr_matrix.loc[row] >= 0] = 0
        corr_matrix.loc[row, corr_matrix.loc[row] < 0] = corr_matrix.loc[row, corr_matrix.loc[row] < 0] / negatives_sum

    # 将对角线上的值设为零
    np.fill_diagonal(corr_matrix.values, 0)

    # 删除全为零的行
    corr_matrix = corr_matrix.loc[(corr_matrix != 0).any(axis=1)]

    return corr_matrix

def compute_stationary_distribution(trans_mat):
    nd = trans_mat.shape[0]
    row_one = np.ones((1, nd))
    I = np.eye(nd)
    ONE = np.ones((nd, nd))
    tmp = I - trans_mat + ONE
    tmp = np.linalg.inv(tmp)
    v = row_one @ tmp
    return v[0, :]

def calculate_relative_returns(scores_df, base_date, days_after):
    # 下载多只股票的数据
    
    tickers = scores_df['Symbol'].tolist()

    # 创建一个空的DataFrame来存储每只股票的相对收益率
    relative_returns_df = pd.DataFrame()

    # 将基准日期和未来日期转换为Timestamp对象
    base_date_timestamp = pd.Timestamp(base_date)
    end_date_timestamp = base_date_timestamp + pd.Timedelta(days=days_after)

    # 下载所有股票基准日期和未来日期的数据
    data = yf.download(tickers, start=base_date_timestamp, end=end_date_timestamp, interval="1d")

    # 遍历每只股票，计算收益率并将其添加到DataFrame
    for ticker in tickers:
        stock_data = data['Adj Close'][ticker]
        base_price = stock_data.iloc[0]  # 基准日期的股票价格
        relative_returns = stock_data / base_price - 1  # 计算每一天的收益率
        relative_returns_df[ticker] = relative_returns  # 将收益率添加到DataFrame，并以股票代码作为列名

    return relative_returns_df



if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: {} <stock_list_file> <target_date> <historical_days> <future_days>".format(sys.argv[0]))
        sys.exit(1)

    stock_list_file = sys.argv[1]
    target_date = sys.argv[2]
    historical_days = int(sys.argv[3])
    future_days = int(sys.argv[4])

    # 计算起始日期
    start_date = pd.to_datetime(target_date) - pd.Timedelta(days=historical_days)
    target_date_timestamp = pd.to_datetime(target_date)
    previous_date = target_date_timestamp - pd.Timedelta(days=1)
    sp500 = pd.read_csv(stock_list_file)
    tickers = sp500['Symbol'].tolist()
    data = yf.download(tickers, start=start_date, end=previous_date, interval="1d")
    price_matrix = data['Adj Close']
    price_matrix = price_matrix.dropna(thresh=10, axis=1)
    updated_tickers = price_matrix.columns.tolist()
    sp500_updated = sp500[sp500['Symbol'].isin(updated_tickers)]
    sp500_updated.to_csv(stock_list_file, index=False)
    # 计算相关性矩阵和稳态分布
    
    corr_matrix = calculate_correlation_matrix(price_matrix)
    v = compute_stationary_distribution(corr_matrix.values)
    syms = corr_matrix.index.values
    sort_id = np.argsort(v)[::-1]
    score_sorted = v[sort_id][:100]
    syms_sorted = syms[sort_id][:100]

    # 保存评分到CSV文件
    scores_df = pd.DataFrame({'Symbol': syms_sorted, 'Score': score_sorted})
    scores_df.to_csv("scores.csv", index=False)

    # 使用新函数计算收益率
    base_date = target_date
    relative_returns_df = calculate_relative_returns(scores_df, base_date, future_days)

    # 打印每只股票未来的最低、最高和总收益率
    for symbol in scores_df['Symbol']:
        min_return = relative_returns_df[symbol].min()
        max_return = relative_returns_df[symbol].max()
        final_return = relative_returns_df[symbol].iloc[-1] 
        print(f"Symbol: {symbol}, Minimum_Return: {min_return:.4f}, Max_Return: {max_return:.4f}, Final_Return: {final_return:.4f}")

    # 重新计算final_returns并重命名列名为'Return'
    final_returns = relative_returns_df.iloc[-1]
    final_returns.rename('Return', inplace=True) 

    # 选取scores_df中'symbol'列对应的股票的得分
    scores = scores_df.set_index('Symbol')['Score']
  
    # 将scores和final_returns合并成一个DataFrame
    scores_and_returns_df = pd.concat([scores, final_returns], axis=1)

    # 计算得分和最终收益率的相关系数矩阵
    correlation_matrix = scores_and_returns_df.corr()

    print("Correlation Matrix between Score and Final Return for Top 100 Stocks:")
    print(correlation_matrix)

    # 绘制所有股票评分的图表
    plt.stem(syms_sorted, score_sorted)
    plt.xlabel('Symbol')
    plt.ylabel('Score')
    plt.title('Stock Rating Ranking')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
