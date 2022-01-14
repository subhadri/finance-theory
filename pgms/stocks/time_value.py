"""
Compute the PV/FV of money for discrete and continuous series
"""

from math import exp
import pandas as pd

def future_discrete_val(x:pd.Series,r:float,n:float) -> pd.Series:
    val: pd.Series = x*(1+r)**n
    return val

def present_discrete_val(x:pd.Series,r:float,n:float) -> pd.Series:
    val: pd.Series = x*(1+r)**-n
    return val

def future_continuous_val(x:pd.Series,r:float,n:float) -> pd.Series:
    val: pd.Series = x*exp(r*n)
    return val

def present_continuous_val(x:pd.Series,r:float,n:float) -> pd.Series:
    val: pd.Series = x*exp(r*n)
    return val

if __name__ == '__main__':
    x = pd.Series([100])
    r = 0.05
    n = 5

    print(f"Future discrete value = {future_discrete_val(x,r,n)}")
    print(f"Present discrete value = {present_discrete_val(x,r,n)}")
    print(f"Future continuous value = {future_continuous_val(x,r,n)}")
    print(f"Present continuous value = {present_continuous_val(x,r,n)}")