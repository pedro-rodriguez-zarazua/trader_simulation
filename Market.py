import Trader as trader
import Stock as stock
import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import norm

class Market:
    def __init__(self, stock_value, stock_share, traders_init_cash, n_traders):
        self.init_stock_value  = stock_value
        self.stock_share       = stock_share
        self.trade_volume      = 0
        self.n_periods         = 200
        
        file_path  = '/Users/pedrorodriguezflores/Documents/Desarrollo/Data/BMV/AC.MX.csv'
        #self.stock             = stock.File_Stock(file_path, self.n_periods)
        self.stock             = stock.Stock(self.init_stock_value, self.stock_share, self.n_periods)
        
        self.n_traders         = n_traders
        self.market_traders    = []
        self.test_traders      = []
        
        for i in range(self.n_traders):
            perfil = [-random.random(), random.random(), random.randint(1,50)]
            self.market_traders.append(trader.Fish(traders_init_cash, self.n_periods, perfil))
        #for i in range(self.n_traders):
            #self.traders.append(trader.Centered(traders_init_cash,self.init_stock_value))

        perfil = [-0.3, 0.5, random.randint(1,9)]
        self.test_traders.append(trader.Fish(traders_init_cash, self.n_periods, perfil))
        #self.test_traders.append(trader.Whale(traders_init_cash, self.n_periods))
        #self.test_traders.append(trader.Value(traders_init_cash, self.n_periods, self.init_stock_value))

        self.day   = self.n_periods
        self.days  = np.arange(self.day - self.n_periods - 1, self.day, 1)
        return None

    def plot_window(self):
        plt.clf()
    
        plt.subplot(3, 1, 1)
        plt.plot(self.days, self.stock.get_historic_price())
        plt.ylabel('Price')
        plt.xticks([])
        plt.tick_params(axis='y', which='both', labelleft = False, labelright = True)
    
        plt.subplot(3, 1, 2)
        plt.plot(self.days, self.stock.get_historic_volume())
        plt.ylabel('Volume')
        plt.xticks([])
        plt.tick_params(axis='y', which='both', labelleft = False, labelright = True)
    
        plt.subplot(3, 1, 3)
        plt.plot(self.days, self.test_traders[0].get_historical())
        plt.ylabel('Trader assets')
        plt.xlabel('time')
        plt.tick_params(axis='y', which='both', labelleft = False, labelright = True)
    
        plt.pause(0.00001)
        return None
    
    def plot_traders(self):
        plt.clf()
        size = len(self.test_traders) + 1
        
        
        for i in range(size - 1):
            plt.subplot(size, 1, i + 1)
            plt.plot(self.days, self.test_traders[i].get_historical())
            plt.ylabel('Trader ' + str(i + 1))
            plt.xticks([])
            plt.tick_params(axis='y', which='both', labelleft = False, labelright = True)
        
        plt.subplot(size, 1, size )
        plt.plot(self.days, self.stock.get_historic_price())
        plt.ylabel('Price')
        plt.tick_params(axis='y', which='both', labelleft = False, labelright = True)
        
        plt.pause(0.00001)
        return None
    
    def ask_order(self, n_stocks):
        stocks_available = self.stock.get_stocks_available()
        if(n_stocks > stocks_available):
            n_stocks = stocks_available
        self.stock.update_stocks_available(-n_stocks)
        return n_stocks

    def take_traders_orders(self):
        sum = 0
        for i in range(len(self.market_traders)):
            n_stocks       = self.market_traders[i].put_order(self.stock.get_price())
            apply_n_stocks = self.ask_order(n_stocks)
            self.market_traders[i].apply_order(apply_n_stocks,self.stock.get_price())
            self.trade_volume  += apply_n_stocks
            
            #print('Trader ' + str(i) + ' assets = ' + str(self.traders[i].get_assets()))
            sum += self.market_traders[i].get_assets()
            #print('Trader ' + str(i) + ' stocks number = ' + str(self.traders[i].get_stocks()))
            #print('Volume trade at trader ' + str(i) + ' = '+ str(self.trade_volume))
        #print('Total cash = ' + str(sum))
        return None


    def run(self):
        while True:
            try:
                
                self.trade_volume     = 0
                self.stock.update_price()
                self.take_traders_orders()
                
                
                for i in range(len(self.test_traders)):
                    n_stocks       = self.test_traders[i].put_order(self.stock.get_price())
                    apply_n_stocks = self.ask_order(n_stocks)
                    self.test_traders[i].apply_order(apply_n_stocks,self.stock.get_price())
                    self.test_traders[i].update_historical()
               
                self.trade_volume  += apply_n_stocks
                volume_percentage  = self.trade_volume/self.stock.get_total_share()
                self.stock.set_price(self.stock.get_price() * (1 + volume_percentage))
                #print('My Trader stocks number = ' + str(self.myTrader.get_stocks()))
                #print('Volume trade percentage= ' + str(self.trade_volume/self.stock_volume))
                
                self.plot_traders()
                
                self.days = np.arange(self.day - self.n_periods - 1, self.day, 1)
                self.day += 1
            except KeyboardInterrupt:
                print("Exiting")
                break
        return None


myMarket = Market(stock_value = 50, stock_share = 1000000, traders_init_cash = 100000, n_traders = 1000)
myMarket.run()


























