import numpy as np
import pandas as pd
from pgms.markowitz.data import NUM_TRADING_DAYS, NUM_PORTFOLIOS, stocks, download_data, calculate_return
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import scipy.optimize as optimization


def portfolio_stat(returns, weights) -> Tuple[float,float,float]:
    portfolio_ret: float = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS
    portfolio_sd: float = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights)))
    sharpe: float = portfolio_ret/portfolio_sd
    return portfolio_ret, portfolio_sd, sharpe

def min_function_sharpe(returns,weights):
    portfolio_means, portfolio_risks, sharpe = portfolio_stat(returns, weights)
    return -sharpe

def optimize_portfolio(returns: pd.DataFrame, weights):
    # sum of weights must be 1
    constraints = {'type': 'eq',
                   'fun': lambda x: np.sum(x) - 1}
    # every weight has to lie between 0 and 1
    bounds = tuple((0,1) for i in range(0,len(stocks)))
    return optimization.minimize(fun=min_function_sharpe, x0=weights[0], args=returns,
                          method='SLSQP', bounds=bounds, constraints=constraints)

def print_optimal_portfolio(optimum):
    print("Optimal portfolio: ", optimum['x'].round(3))


def generate_portfolios(returns) -> Tuple[List[np.ndarray], pd.Series, pd.Series]:

    portfolio_weights: List[np.ndarray] = [np.random.random(len(stocks)) for i in range(0,NUM_PORTFOLIOS)]
    portfolio_weights_norm: List[np.ndarray] = [w/np.sum(w) for w in portfolio_weights]
    stat = [portfolio_stat(returns, w) for w in portfolio_weights_norm]
    portfolio_means: pd.Series = pd.Series([p[0] for p in stat])
    portfolio_risks: pd.Series = pd.Series([p[1] for p in stat])
    return portfolio_weights_norm, portfolio_means, portfolio_risks

def show_portfolios(opt, ret, returns, risks):
    plt.figure(figsize=(10,6))
    plt.scatter(risks, returns, c=returns/risks, marker='o')
    plt.grid(True)
    plt.xlabel('Expected volatility')
    plt.ylabel('Expected return')
    plt.colorbar(label='Sharpe Ratio')
    plt.show(portfolio_stat(opt['x'],ret)[2],portfolio_stat(opt['x'],ret)[1],'g*',markersize=20.)
    plt.show()

if __name__ == '__main__':
    data = download_data()
    returns = calculate_return(data)
    weights, means, risks = generate_portfolios(returns)
    p = optimize_portfolio(returns,weights)
    show_portfolios(p,returns,means,risks)
    print('Done')