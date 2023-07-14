import yfinance as yf
import pandas as pd

# 下载多个股票的数据
sp500 = pd.read_csv(r'C:\Users\Administrator\Desktop\stock\constituents_csv.csv')#括号内为csv文件存储位置
tickers = sp500['Symbol'].tolist()
data_dict = yf.download(tickers, start="2023-01-01", end="2023-6-31", interval="1d")
