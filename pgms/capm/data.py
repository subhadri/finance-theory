import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

RISKFREE_RATE = 0.05
MONTHS_IN_YEAR = 12

class CAPM:

    def __init__(self, stocks, start_date, end_date):
        self.data = None
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date

    def download_data(self):
        data = {}
        for stock in self.stocks:
            ticker = yf.download(stock,self.start_date,self.end_date)
            data[stock] = ticker['Adj Close']
        return pd.DataFrame(data)

    def calculate_beta(self):
        d = self.data
        covmat = np.cov(d['s_returns'], d['m_returns'])
        beta = covmat[0,1] / covmat[1,1]
        print('Systematic risk:', beta)

    def regression(self):
        beta,alpha = np.polyfit(self.data['m_returns'],self.data['s_returns'],deg=1)
        expected_return = RISKFREE_RATE + beta * (self.data['m_returns'].mean()*MONTHS_IN_YEAR - RISKFREE_RATE)
        print("Expected return = ", expected_return)
        self.plot_regression(alpha,beta)

    def plot_regression(self,alpha,beta):
        fig, ax = plt.subplots(1,figsize=(20,10))
        ax.scatter(self.data['m_returns'], self.data['s_returns'], label='Data points')
        ax.plot(self.data['m_returns'], beta*self.data['m_returns'] + alpha, color='red')
        plt.title('CAPM: finding alphas and betas')
        plt.text(0.08,0.05, r'$R_a = \beta * R_m + \alpha$', fontsize=18)
        plt.legend()
        plt.grid(True)
        plt.show()

    def initialize(self):
        stock_data = self.download_data()
        stocks_data = stock_data.resample('M').last()
        self.data = pd.DataFrame({'s_adjclose': stocks_data[self.stocks[0]],
                                  'm_adjclose': stocks_data[self.stocks[1]]})
        # logarithmic monthly returns
        self.data[['s_returns','m_returns']] = np.log(self.data[['s_adjclose','m_adjclose']] /
                                                      self.data[['s_adjclose','m_adjclose']].shift(1))
        self.data = self.data[1:]
        print(self.data)



if __name__ == '__main__':
    capm = CAPM(['IBM','^GSPC'], '2010-01-01', '2017-01-01')
    capm.initialize()
    capm.calculate_beta()
    capm.regression()