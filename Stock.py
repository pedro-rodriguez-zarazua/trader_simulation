import random
import csv
import numpy as np
from scipy.stats import norm


class Stock():
    def __init__(self, ini_price, total_share, n_periods):
        self.price            = ini_price
        self.total_share      = total_share
        self.stocks_available = total_share
        self.volatility       = random.randint(1, 6)
        self.historic_price   = [self.price]
        self.historic_volume  = [self.stocks_available]
        self.n_periods        = n_periods
        self.day              = 0
        self.high_volatility  = False
        
        for i in range(self.n_periods):
            self.update_price()
            self.historic_price.append(self.get_price())
            self.historic_volume.append(self.get_stocks_available())
            self.day += 1
        return None

    def set_price(self, price):
        self.price = price
        if(self.price < 1):
            self.price = 1
        return None

    def update_stocks_available(self, update):
        self.stocks_available += update
        self.historic_volume.append(self.stocks_available)
        self.historic_volume.pop(0)
        return None
    
    def get_stocks_available(self):
        return self.stocks_available
    
    def get_price(self):
        return self.price

    def get_total_share(self):
        return self.total_share

    def update_price(self):
        r = random.random()
        if(r < 0.95 and self.high_volatility == False):
            self.high_volatility = False
            volatility  = random.randint(1, 7)
        else:
            self.high_volatility = True
            volatility = random.randint(7, 14)

        if(self.high_volatility == True):
            r = random.random()
            if(r < 0.3):
                self.high_volatility = False

        noise = norm.rvs(size=1, loc=0, scale=volatility)
        if(noise < 0 and (self.price + noise) < 1):
            noise *= -1
        
        seasonality = np.sin(self.day*0.05)
        self.set_price(self.price + noise + seasonality)
        self.historic_price.append(self.price)
        self.historic_price.pop(0)
        self.day += 1
        return None

    def get_historic_price(self):
        return self.historic_price
    def get_historic_volume(self):
        return self.historic_volume


class File_Stock():
    def __init__(self, file_path, n_periods):
        self.close = []
        self.volume= []
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    if(row[4] != 'null'):
                        self.close.append(float(row[4]))
                    else:
                        self.close.append(self.close[len(self.close) - 1])
                    if(row[6] != 'null'):
                        self.volume.append(float(row[6]))
                    else:
                        self.volume.append(self.volume[len(self.volume) - 1])
                    line_count += 1
            print(f'Processed {line_count} lines.')
                
        self.price            = self.close[0]
        self.stocks_available = self.volume[0]
        self.total_share      = 10000000
        self.historic_price   = [self.close[0]]
        self.historic_volume  = [self.volume[0]]
        self.n_periods        = n_periods
        self.day              = 0
        for i in range(self.n_periods):
            self.historic_price.append(self.close[i])
            self.historic_volume.append(self.volume[i])
            self.day += 1
        return None

    def set_price(self, dummy):
        if(self.price < 1):
            self.price = 1
        return None
            
    def update_stocks_available(self, dummy):
        self.stocks_available = self.volume[self.day]
        self.historic_volume.append(self.stocks_available)
        self.historic_volume.pop(0)
        return None

    def update_price(self):
        self.price = self.close[self.day]
        self.historic_price.append(self.price)
        self.historic_price.pop(0)
        self.day += 1
        return None

    def get_total_share(self):
        return self.total_share
    
    def get_stocks_available(self):
        return self.stocks_available
    
    def get_price(self):
        return self.price

    def get_historic_price(self):
        return self.historic_price
    def get_historic_volume(self):
        return self.historic_volume



















