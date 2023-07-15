import yfinance as yf
import pandas as pd

# 下载500只股票近3个月的价格并剔除无法生成价格和生成价格数量少于10个的股票
def download_stock_prices():
    sp500 = pd.read_csv(r'C:\Users\Administrator\Desktop\stock\constituents_csv.csv')#括号内为csv文件存储位置
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


# 下载股票价格
stock_prices = download_stock_prices()

# 保存为CSV文件
csv_file_path = r'C:\Users\Administrator\Desktop\stock\stock_prices.csv'
stock_prices.to_csv(csv_file_path)

print("股票价格已保存到CSV文件:", csv_file_path)
