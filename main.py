import models
import yfinance
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from pydantic import BaseModel 
from models import Stock
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)    #create database here

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
def home(request: Request, forward_pe = None, dividend_yield = None, ma50 = None, ma200 = None, db: Session = Depends(get_db)):
    """
    show all stocks in the database and button to add more
    button next to each stock to delete from database
    filters to filter this list of stocks
    button next to each to add a note or save for later
    """

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

    return templates.TemplateResponse("home.html", {
        "request": request, 
        "stocks": stocks, 
        "dividend_yield": dividend_yield,
        "forward_pe": forward_pe,
        "ma200": ma200,
        "ma50": ma50
    })


def fetch_stock_data(id: int):
    
    db = SessionLocal()

    stock = db.query(Stock).filter(Stock.id == id).first()

    yahoo_data = yfinance.Ticker(stock.symbol)

    stock.ma200 = yahoo_data.info['twoHundredDayAverage']
    stock.ma50 = yahoo_data.info['fiftyDayAverage']
    stock.price = yahoo_data.info['previousClose']
    stock.forward_pe = yahoo_data.info['forwardPE']
    stock.forward_eps = yahoo_data.info['forwardEps']
    stock.profit_margins = yahoo_data.info['profitMargins']
    stock.operating_margins = yahoo_data.info['operatingMargins']
    stock.ebitda = yahoo_data.info['ebitda']
    stock.shortName = yahoo_data.info['shortName']
    stock.shares_outstanding = yahoo_data.info['sharesOutstanding']
    stock.r_on_assets = yahoo_data.info['returnOnAssets']
    stock.r_on_equity = yahoo_data.info['returnOnAssets']
    stock.total_revenue = yahoo_data.info['totalRevenue']
    stock.dividend_yield = yahoo_data.info['dividendYield']
    stock.debt_to_equity = yahoo_data.info['dividendYield']


    db.add(stock)
    db.commit()


@app.post("/stock")
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    add one or more tickers to the database
    background task to use yfinance and load key statistics
    """

    stock = Stock()
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()

    background_tasks.add_task(fetch_stock_data, stock.id)

    return {
        "code": "success",
        "message": "stock was added to the database"
    }


print('How Significant are You in the grand scheme of things')