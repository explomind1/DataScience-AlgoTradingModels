from typing import Optional
import models
import yfinance
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from pydantic import BaseModel
from models import Stock
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

class StockRequest(BaseModel):
    symbol: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



@app.get("/")
def Dashboard(request: Request,forward_pe = None, dividend_yield = None, ma50 = None, ma200 = None, db: Session = Depends(get_db)):
    '''
        This the dashboard!
    '''
    stocks = db.query(Stock)
    if forward_pe:
        stocks = stocks.filter(Stock.forward_pe < forward_pe)

    if dividend_yield:
        stocks = stocks.filter(Stock.dividend_yield > dividend_yield)
    
    if ma50:
        stocks = stocks.filter(Stock.price > Stock.ma50)
    
    if ma200:
        stocks = stocks.filter(Stock.price > Stock.ma200)
    
    stocks = stocks.all()
    

    return templates.TemplateResponse("dashboard.html",
    {"request":request,
     "stocks": stocks,
    "dividend_yield": dividend_yield,
    "forward_pe": forward_pe,
    "ma200": ma200,
    "ma50": ma50  })

   

    

def fetch_stock_data(id: int):
    
    db = SessionLocal()
    stock = db.query(Stock).filter(Stock.id == id).first()

    stock = db.query(Stock).filter(Stock.id == id).first()

    yahoo_data = yfinance.Ticker(stock.symbol)

    stock.ma200 = yahoo_data.info['twoHundredDayAverage']
    stock.ma50 = yahoo_data.info['fiftyDayAverage']
    stock.price = yahoo_data.info['previousClose']
    stock.forward_pe = yahoo_data.info['forwardPE']
    stock.forward_eps = yahoo_data.info['forwardEps']
    if yahoo_data.info['dividendYield'] is not None:
        stock.dividend_yield = yahoo_data.info['dividendYield'] * 100

    db.add(stock)
    db.commit()



@app.post("/stock")
async def create_stock(stockrequest:StockRequest,background_tasks: BackgroundTasks,db: Session = Depends(get_db)):
    """
    add one or more tickers to the database
    background task to use yfinance and load key statistics
    """

    stock = Stock()
    stock.symbol = stockrequest.symbol
    db.add(stock)
    db.commit()

    background_tasks.add_task(fetch_stock_data, stock.id)
    return {
        "code": "Success",
        "messeage": "Stock Created"
    }



