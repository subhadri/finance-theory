'''
Download stock prices from Yahoo finance, compute returns and plot basic trend plots
'''

import numpy as np
import yfinance as yahoo
import pandas as pd
import matplotlib.pyplot as plt

stocks = ['AAPL','WMT','TSLA','GE','AMZN','DB']
start_date = '2010-01-01'
end_date = '2017-01-01'
NUM_TRADING_DAYS = 252
NUM_PORTFOLIOS = 10000

def download_data():
    stock_data = {}

    for stock in stocks:
        ticker = yahoo.Ticker(stock)
        stock_data[stock] = ticker.history(start=start_date,end=end_date)['Close']

    return pd.DataFrame(stock_data)

def show_data(data):
    data.plot(figsize=(10,5))
    plt.show()

def calculate_return(data):
    log_return = np.log(data/data.shift(1))
    return log_return[1:]

def show_statistics(returns):
    print(returns.mean() * NUM_TRADING_DAYS)
    print(returns.cov() * NUM_TRADING_DAYS)

if __name__ == '__main__':
    data = download_data()
    returns = calculate_return(data)
    show_statistics(returns)