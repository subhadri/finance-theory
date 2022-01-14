'''
Calculate the prices of zero-coupon and coupon-bearing bonds
'''

from math import exp

class ZeroCouponBonds:

    def __init__(self,fv,t,r):
        self.fv = fv
        self.t = t
        self.r = r/100

    def present_value(self,x,n):
        return x*exp(-self.r*n)

    def calc_price(self):
        return self.present_value(self.fv,self.t)

class CouponBond:

    def __init__(self,principal,coupon_rate,maturity,interest_rate):
        self.principal = principal
        self.coupon_rate = coupon_rate / 100
        self.maturity = maturity
        self.interest_rate = interest_rate / 100

    def present_value(self,x,n):
        return x*exp(self.interest_rate*n)

    def calculate_price(self):
        price = 0
        # discount the coupon payments
        for t in (1, self.maturity+1):
            price = price + self.present_value(self.principal * self.coupon_rate, t)

        price = price + self.present_value(self.principal,self.maturity)
        return price


if __name__ == '__main__':

    zcb = ZeroCouponBonds(1000,2,4)
    print(f"Price of bond = {zcb.calc_price()}")

    cb = CouponBond(1000,10,2,4)
    print(f"Price of coupon bond = {cb.calculate_price()}")