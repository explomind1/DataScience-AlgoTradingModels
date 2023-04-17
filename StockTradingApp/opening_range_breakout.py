import sqlite3,Config
import alpaca_trade_api as tradeapi
from datetime import date
import yfinance
import smtplib, ssl



# Create a secure SSL context
context = ssl.create_default_context()

connection = sqlite3.connect(Config.DB_PATH) 
connection.row_factory= sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    select id from strategy where name = 'opening_range_breakout'

""")

strategy_id= cursor.fetchone()["id"]

cursor.execute("""
    select symbol,name
    from stock
    join stock_strategy on stock_strategy.stock_id =stock.id
    where stock_strategy.strategy_id= ?

""",(strategy_id, ))

stocks= cursor.fetchall()

symbols=[stock["symbol"] for stock in stocks]

current_date= date.today().isoformat()
#current_date= '2021-03-05'
start_minute_bar=f'{current_date} 9:30:00-05:00'
end_minute_bar= f'{current_date} 9:45:00-05:00'

api = tradeapi.REST(Config.API_KEY, Config.SECRET_KEY, base_url=Config.API_URL)

orders= api.list_orders(status= "all" ,limit=500, after=f"{current_date}T14:30:00Z")
#orders= api.list_orders(status= "all" ,limit=500)

#orders= api.list_orders(status= "open", limit=500)
# positions = api.list_positions()
# print("here are the positions!")
# print(positions)


existing_order_symbols= [order.symbol for order in orders]
print(" here are the existing order symbols")
print(existing_order_symbols)




# alpaca get_barset does not have proper one min values!!!(especially the first 15 min)
# for symbol in symbols: 
#      # minute_bars= api.polygon.historic_agg_v2(symbol,1,'minute', _from= '2021-3-5', to='2021-3-5').df


#     minute_bars= api.get_barset(symbol, '1Min', start= "2021-03-05", end="2021-03-05").df

#     opening_range_mask= (minute_bars.index >= start_minute_bar) & (minute_bars.index < end_minute_bar)
#     #opening_range_bars= minute_bars.loc[opening_range_mask] 
#     print(symbol)
#     #print(opening_range_bars)
#     print(minute_bars)
    
#much better accuracy:


messages=[]

for symbol in symbols:
    minute_bars=yfinance.Ticker(symbol).history(interval='1m',period="2d")
    #minute_bars=yfinance.Ticker(symbol).history(interval='1m',start='current_date',end='current_date')

    opening_range_mask= (minute_bars.index >= start_minute_bar) & (minute_bars.index < end_minute_bar)
    opening_range_bars= minute_bars.loc[opening_range_mask] 
    print(symbol)
   # print(opening_range_bars)
    opening_range_low= opening_range_bars['Low'].min()
    opening_range_high=opening_range_bars['High'].max()
    opening_range= opening_range_high - opening_range_low
    print(opening_range_high,opening_range_low)
    #print( "this is the opening range")
    #print(opening_range)
   
    after_opening_range_mask= minute_bars.index >= end_minute_bar
    after_opening_range_bars =minute_bars.loc[after_opening_range_mask]


    after_opening_range_breakout= after_opening_range_bars[after_opening_range_bars['Close'] > opening_range_high]
    if not after_opening_range_breakout.empty:
        print("not empty")
        if symbol not in existing_order_symbols:
            #print(after_opening_range_breakout) 
            #global limit_price
            limit_price= after_opening_range_breakout.iloc[0]["Close"]
            #print("limit price :")
            #print(limit_price)
            messages.append(f"placing order for {symbol} at {limit_price}, closed_above {opening_range_high}\n\n {after_opening_range_breakout.iloc[0]}\n\n")
            print(" ")
            #print(f"placing order for {symbol} at {limit_price}, closed_above {opening_range_high}\n\n {after_opening_range_breakout.iloc[0]}\n\n")

    
 
            if not limit_price == limit_price + opening_range:
                
                api.submit_order(
                symbol=symbol,
                qty=10,
                side='buy',
                type='limit',
                time_in_force='day',
                order_class='bracket',
                limit_price= limit_price,
                take_profit= dict(
                    limit_price= limit_price + opening_range,
                ),
                stop_loss= dict(
                    stop_price=limit_price - opening_range,
                )

            )
            else:
                print(f"Invalid OBR {symbol}, skipping!")
        else:
            print(f"Already an order for {symbol}, skipping!")


if not limit_price == limit_price + opening_range:
    print(messages)
    if messages:
        with smtplib.SMTP_SSL(Config.EMAIL_HOST, Config.EMAIL_PORT, context=context) as server:

            server.login(Config.EMAIL_ADRESS, Config.EMAIL_PASSWORD)

            email_message = f"Subject: Trade Notifications for {current_date}\n\n"
            email_message += "\n\n".join(messages) 
            

            server.sendmail(Config.EMAIL_ADRESS, Config.EMAIL_ADRESS, email_message)