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
#import datetime as dt
import talib as ta
from itertools import compress
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.signal
# import warnings
# warnings.simplefilter("ignore")
import math
#from ipynb.fs.full.Hide import hide_toggle
import sqlite3
import alpaca_trade_api as tradeapi

connection = sqlite3.connect(Config.DB_PATH) #connection = sqlite3.connect('app.db') 

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL,
        exchange TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_price (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        open NOT NULL, 
        high NOT NULL, 
        low NOT NULL, 
        close NOT NULL, 
        volume NOT NULL,
        sma_20,
        sma_50,
        rsi_14,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS strategy (
        id INTEGER PRIMARY KEY, 
        name NOT NULL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_strategy (
        stock_id INTEGER NOT NULL, 
        strategy_id INTEGER NOT NULL,
        FOREIGN KEY(stock_id) REFERENCES stock (id)
        FOREIGN KEY(strategy_id) REFERENCES strategy (id)
        UNIQUE(stock_id,strategy_id)
        
    )
""")


 

strategies= ['opening_range_breakout','opening_range_breakdown','Divergence']

for strategy in strategies:
    cursor.execute("""
        INSERT INTO strategy (name) VALUES (?)
    """, (strategy,))

connection.commit()