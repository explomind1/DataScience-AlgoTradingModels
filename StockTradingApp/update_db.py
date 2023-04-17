import pandas as pd 
import numpy as np
import yfinance
from IPython.display import HTML
import random
#from ipynb.fs.full.Functions1 import hide_toggle
#from operator import itemgetter 
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
#from mpl_finance import candlestick_ohlc
from mplfinance.original_flavor import candlestick_ohlc
import pandas_datareader as pdr
from datetime import datetime as dt
import datetime
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
import Config 




connection = sqlite3.connect(Config.DB_PATH) #connection = sqlite3.connect('app.db') 
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, name FROM stock
""")
rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows] # list comprehension



api = tradeapi.REST(Config.API_KEY, Config.SECRET_KEY, base_url=Config.API_URL) # or use ENV Vars shown below
assets = api.list_assets()


print(dt.today().isoformat())
for asset in assets:
    #  if asset.symbol == "APH" :
    #      print(asset)
    try:
        if asset.status =='active' and asset.tradable and asset.fractionable and asset.symbol not in symbols:
            print(f"Added a new stock:{asset.symbol}")
            cursor.execute("""
                    INSERT INTO stock (symbol, name, exchange)
                    VALUES (?, ?, ?)
            """, (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
            print(asset.symbol)
            print(e)
            
connection.commit()
# delete from stock where id >9520;
# crontab -e ext ls -al rm populate log!
# shortable
# sset.fractionable