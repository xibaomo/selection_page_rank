import yfinance as yf
import pandas as pd

# 下载500只股票近3个月的价格并剔除无法生成价格和生成价格数量少于10个的股票
def download_stock_prices():
    sp500 = pd.read_csv(r'C:\Users\Administrator\Desktop\股票相关资料\constituents_csv.csv')#括号内为csv文件存储位置
    symbols = sp500['Symbol'].tolist()
    start_date = pd.Timestamp.now() - pd.DateOffset(months=3)
    end_date = pd.Timestamp.now()
    stock_prices = pd.DataFrame()

    for symbol in symbols:
        try:
            data = yf.download(symbol, start=start_date, end=end_date)
            if len(data) >= 10:
                stock_prices[symbol] = data['Close']
        except Exception as e:
            print(f"Failed to download data for {symbol}: {e}")
            
    
    
    return stock_prices

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
# 下载股票价格
stock_prices = download_stock_prices()

# 生成相关系数矩阵
correlation_matrix = calculate_correlation_matrix(stock_prices)

transition_matrix = create_transition_matrix(correlation_matrix, threshold=-0.7)
# 打印相关系数矩阵
print("相关系数矩阵:")
print(correlation_matrix)
print("归一化矩阵:")
print(transition_matrix)
