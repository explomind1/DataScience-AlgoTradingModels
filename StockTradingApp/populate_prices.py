
import pandas as pd 
import numpy as np
import yfinance
from IPython.display import HTML
import random
import Config
#from ipynb.fs.full.Functions1 import hide_toggle
#from operator import itemgetter 
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
#from mpl_finance import candlestick_ohlc
from mplfinance.original_flavor import candlestick_ohlc
import pandas_datareader as pdr
import datetime as dt
from datetime import date
import talib as ta
from itertools import compress
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.signal
# import warnings
# warnings.simplefilter("ignore")
import math
#from opening_range_breakout import current_date
#from ipynb.fs.full.Hide import hide_toggle
import sqlite3
import alpaca_trade_api as tradeapi
import tulipy as ti


connection = sqlite3.connect(Config.DB_PATH)

connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute("""
    SELECT id, symbol, name FROM stock
""")
rows = cursor.fetchall()
symbols = []

stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']
api = tradeapi.REST(Config.API_KEY, Config.SECRET_KEY, base_url= Config.API_URL) # or use ENV Vars shown below

chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
    barsets = api.get_barset(symbol_chunk, 'day')

    for symbol in barsets:
        #print(barsets[symbol])
        recent_close=[bar.c for bar in barsets[symbol]]
        recent_close_date=[bar.t.date() for bar in barsets[symbol]]
        #recent_close= np.array(recent_close) this doesnt work!
        # if len(recent_close)>= 200:
        #     sma_200= ti.sma(np.array(recent_close), period= 200)   free alpaca Api does not give more than 100 days for daily! 
        #print(f"processing symbol {symbol}")
# from datetime import datetime as dt
# import datetime

# print(dt.today().isoformat())

# all=[]
# for bar in barsets[symbol]:
#     all.append(bar.t.date())
# print(all[-1])
        for bar in barsets[symbol]:
            stock_id = stock_dict[symbol]
            #if len(recent_close)>= 50 and date.today().isoformat() == bar.t.date().isoformat():
            if len(recent_close)>= 50 and '2021-03-10' == bar.t.date().isoformat():

                sma_20= ti.sma(np.array(recent_close), period= 20)[-1]
                sma_50= ti.sma(np.array(recent_close), period= 50)[-1]
                rsi_14= ti.rsi(np.array(recent_close), period= 14)[-1]
             
            else:
                sma_20,sma_50,rsi_14 = None,None,None

            cursor.execute("""
                INSERT INTO stock_price (stock_id, date, open, high, low, close, volume, sma_20, sma_50, rsi_14)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v, sma_20, sma_50, rsi_14))
connection.commit()