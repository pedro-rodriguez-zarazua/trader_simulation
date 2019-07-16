import Market as market



myMarket = market.Market(stock_value = 1000, stock_volume = 10000, traders_init_cash = 10000, n_traders = 10)
myMarket.run()
