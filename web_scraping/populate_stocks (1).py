import config_cloud
import csv
import alpaca_trade_api as tradeapi
import psycopg2, psycopg2.extras
from datetime import datetime as dt

connection = psycopg2.connect(host=config_cloud.DB_HOST_cloud,password=config_cloud.DB_PASS_cloud,database= config_cloud.DB_NAME_cloud,user=config_cloud.DB_USER_cloud,port=config_cloud.DB_PORT_cloud)

cursor= connection.cursor(cursor_factory= psycopg2.extras.DictCursor)

cursor.execute("SELECT * from hotteststocks")

stocks= cursor.fetchall()

for stock in stocks:
    print(stock["symbol"])

cursor.execute("""
    SELECT symbol, name FROM hotteststocks
""")
rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows] 

api = tradeapi.REST(config_cloud.API_KEY, config_cloud.SECRET_KEY, base_url=config_cloud.API_URL) 
assets = api.list_assets()
# list1=[]
# for asset in assets:
#     if asset.status =='active' and asset.tradable and asset.shortable and asset.marginable and asset.fractionable and asset.symbol not in symbols:
#         list1.append(asset)



print(dt.today()) #4K main stocks--
for asset in assets:
    try:
        if asset.status =='active' and asset.tradable and asset.shortable and asset.marginable and asset.fractionable and asset.symbol not in symbols:
            print(f"Added a new stock:{asset.symbol}")
            cursor.execute("""
                    INSERT INTO hotteststocks (symbol, name, exchange, is_etf)
                    VALUES (%s, %s, %s, false)
                """, (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
            print(asset.symbol)
            print(e)
            
            
connection.commit()