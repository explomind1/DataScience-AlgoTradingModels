import config_cloud
import csv
import alpaca_trade_api as tradeapi
import psycopg2, psycopg2.extras
from datetime import datetime as dt
import plotly.graph_objects as go
import plotly.io as pio


connection = psycopg2.connect(host=config_cloud.DB_HOST_cloud,password=config_cloud.DB_PASS_cloud,database= config_cloud.DB_NAME_cloud,user=config_cloud.DB_USER_cloud,port=config_cloud.DB_PORT_cloud)

cursor= connection.cursor(cursor_factory= psycopg2.extras.DictCursor)

cursor.execute("select count(*) as num_mentions,stock_id,symbol from mention_wallstreet join hotteststocks on hotteststocks.id = mention_wallstreet.stock_id group by stock_id,symbol order by num_mentions desc limit 5")
# display it on explomind.io webscraping subtitle then delete it for tomorrows
stocks_wallstreet= cursor.fetchall()

cursor.execute("select count(*) as num_mentions,stock_id,symbol from mention_stocks join hotteststocks on hotteststocks.id = mention_stocks.stock_id group by stock_id,symbol order by num_mentions desc limit 5")
# display it on explomind.io webscraping subtitle then delete it for tomorrows
stocks_stocks= cursor.fetchall()


#cursor.execute("delete from mention")

hotteststocks_wallstreet=[]
for i in stocks_wallstreet:
    hotteststocks_wallstreet.append(i[2])
hotteststocks_values1=[]
for i in stocks_wallstreet:
    hotteststocks_values1.append(i[0])

hotteststocks_stocks=[]
for i in stocks_stocks:
    hotteststocks_stocks.append(i[2])
hotteststocks_values2=[]
for i in stocks_stocks:
    hotteststocks_values2.append(i[0])

fig = go.Figure( data=[
    go.Bar(name='/WallStreetBets', x=hotteststocks_wallstreet, y=hotteststocks_values1),
    go.Bar(name='/Stocks', x=hotteststocks_stocks, y=hotteststocks_values2)
])
# Change the bar mode

fig.update_layout(
    title='WallStreetBets-Stocks Subreddit Scraping',
    title_font_size=22,
    xaxis_tickfont_size=18,
    yaxis=dict(
        title='Number of Mentions',
        titlefont_size=18,
        tickfont_size=18,
    ),
    barmode='group',legend = dict(font = dict(family = "Courier", size = 20, color = "black")),
                  legend_title = dict(font = dict(family = "Courier", size = 30, color = "blue"))
    
)

pio.write_html(fig, file="plotly_webscraping.html", auto_open=True)

fig.show()

