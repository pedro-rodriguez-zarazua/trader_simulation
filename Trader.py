import numpy as np
import random
from scipy.stats import norm

class Trader:
    def __init__(self, init_cash, n_periods):
        self.init_cash  = init_cash
        self.cash       = init_cash
        self.assets     = init_cash
        self.profit     = 0
        self.stocks     = 0
        self.comission  = 0 # 0.001
        self.n_periods  = n_periods
        self.historical = [self.assets]
        for i in range(self.n_periods):
            self.historical.append(self.profit)
        return None
    def get_stocks(self):
        return self.stocks
    def get_cash(self):
        return self.cash
    def get_assets(self):
        return self.assets
    def get_profit(self):
        return self.profit
    def set_assets(self, price):
        self.assets = self.cash + (price*self.stocks)
        self.profit = 100 * (self.assets - self.init_cash) / self.init_cash
        return None
    def set_stocks(self, num):
        self.stocks += num
        return None
    def set_cash(self, earning):
        self.cash += earning
        return None
    def update_historical(self):
        self.historical.append(self.get_profit())
        self.historical.pop(0)
        return None
    def get_historical(self):
        return self.historical
    def apply_order(self, stock_num, price):
        if(stock_num > 0):
            cost_gain    = -stock_num * price * (1 + self.comission)
        else:
            cost_gain    = -stock_num * price * (1 - self.comission)
        self.stocks += stock_num
        self.cash   += cost_gain
        self.set_assets(price)
        return None

class Fish(Trader):
    def __init__(self, init_cash, n_periods, perfil = [-0.5,0.5, 5]):
        Trader.__init__(self, init_cash, n_periods)
        self.perfil = perfil
        return None
    def buy(self, price):
        cashin_stock = int(self.cash/price)
        if(cashin_stock > 1):
            stock_num = random.randint(1,self.perfil[2])
            if(cashin_stock < stock_num):
                stock_num = cashin_stock
        else:
            stock_num = 0
        return stock_num
    def sell(self, price):
        if(self.stocks > 0):
            stock_num = random.randint(1, self.perfil[2])
            if(self.stocks < stock_num):
                stock_num = self.stocks
        else:
            stock_num = 0
        return -stock_num
    def put_order(self,price):
        if(price > 10):
            r = (2 * random.random()) - 1
            stock_num = 0
            if(r < self.perfil[0]):
                stock_num = self.sell(price)
            elif(r > self.perfil[1]):
                stock_num = self.buy(price)
        else:
            stock_num = int((self.cash/price)/3)
        if(stock_num * price > self.cash):
            stock_num = int(self.cash/price)
        return stock_num

class Whale(Trader):
    def put_order(self,price):
        if(self.cash > price):
            stock_num = 1
        else:
            stock_num = -self.stocks
        return stock_num

class Value(Trader):
    def __init__(self, init_cash, n_periods, value):
        Trader.__init__(self, init_cash, n_periods)
        self.value = value
        return None
    
    def put_order(self,price):
        stock_num = 0
        if(price < 0.7 * self.value):
            stock_num = int(10 * (1 - (price/self.value)))
        elif(price > 1.3 * self.value):
            stock_num = int(10 * ((price/self.value) - 1))
        if(stock_num * price > self.cash):
            stock_num = int(self.cash/price)
        return stock_num

