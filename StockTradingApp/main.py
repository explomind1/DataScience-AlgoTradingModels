from fastapi import FastAPI,Request,Form
import sqlite3,Config
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from datetime import date

app= FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def Dashboard(request: Request):
    connection = sqlite3.connect(Config.DB_PATH) 

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    
    stock_filter = request.query_params.get('filter',False)

    stock_filter_rsi = request.query_params.get('RSI Filter',False)

    if stock_filter == "new_closing_highs":

        cursor.execute("""   
        select * from (
        select symbol, name, stock_id,max(close),date
        from stock_price join stock on stock.id=stock_price.stock_id
        group by stock_id
        order by symbol 
        ) where date = (select max(date) from stock_price)
        """)

    elif stock_filter == "new_closing_lows":

        cursor.execute("""   
        select * from (
        select symbol, name, stock_id,min(close),date
        from stock_price join stock on stock.id=stock_price.stock_id
        group by stock_id
        order by symbol 
        ) where date = (select max(date) from stock_price)
        """)


    elif stock_filter_rsi =="RSI30":

        cursor.execute("""   
        select symbol,name, close, rsi_14,sma_20,sma_50
        from stock join stock_price on stock_price.stock_id=stock.id
        where date ="2021-03-10" and rsi_14<30;
        """)
    elif stock_filter_rsi =="RSI70":

        cursor.execute("""   
        select symbol,name, close, rsi_14,sma_20,sma_50
        from stock join stock_price on stock_price.stock_id=stock.id
        where date ="2021-03-10" and rsi_14>70;
        """)


        # bearish_count= cursor.execute("""   
        # select count(*) from (
        # select symbol, name, stock_id,min(close),date
        # from stock_price join stock on stock.id=stock_price.stock_id
        # group by stock_id
        # order by symbol 
        # ) where date = (select max(date) from stock_price)
        # """)
        # bearish_count= cursor.fetchall()
        # print(bearish_count)   
    else:
        

        cursor.execute("""
            SELECT id,symbol, name FROM stock ORDER BY symbol
        """)

    rows = cursor.fetchall()
    # u should modify the date below! as date.today().isoformat() after 5;30 till 12 istanbul time

    cursor.execute("""
        select symbol, rsi_14,sma_20,sma_50,close
        from stock join stock_price on stock_price.stock_id=stock.id
        where date ="2021-03-10";  
    """)

    indicator_rows= cursor.fetchall()
    indicator_values={}

    for row in indicator_rows:
        indicator_values[row['symbol']]= row


    return templates.TemplateResponse("index.html",
    {"request":request,
    "stocks":rows,
    #  "bearish_count= ":bearish_count
    "indicator_values": indicator_values
    })
@app.get("/stock/{symbol}")
def StockDetail(request: Request,symbol ):
    connection = sqlite3.connect(Config.DB_PATH) 
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM strategy
    """)

    strategies = cursor.fetchall()


    cursor.execute("""
        SELECT id,symbol, name FROM stock WHERE symbol=? 
    """,( symbol,))

    row = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id=? ORDER BY date DESC
    """,(row['id'],))

    prices = cursor.fetchall()

    return templates.TemplateResponse("stock_detail.html",
    {"request":request,
    "stock":row,
    "bars": prices,
    "strategies": strategies
    })

@app.post("/apply_strategy")
def apply_strategy(strategy_id: int = Form(...), stock_id: int = Form(...)):
    connection = sqlite3.connect(Config.DB_PATH) 
    #connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?,?) 
    """, (stock_id, strategy_id))

    connection.commit()

    return RedirectResponse(url=f"/strategy/{strategy_id}",status_code=303)

@app.get("/strategy/{strategy_id}")
def strategy(request : Request, strategy_id):
    connection = sqlite3.connect(Config.DB_PATH) 
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name
        FROM strategy
        WHERE id = ?
    """, (strategy_id,))

    strategy= cursor.fetchone()

    cursor.execute("""
        SELECT symbol, name
        FROM stock JOIN stock_strategy on stock_strategy.stock_id = stock.id
        WHERE strategy_id = ?
    """,  (strategy_id, ))

    stocks= cursor.fetchall() 


    return templates.TemplateResponse("strategy.html", {"request": request, "stocks":stocks, "strategy": strategy })






