from sqlalchemy import Boolean, Column, ForeignKey, Numeric, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    price = Column(Numeric(10, 2))
    forward_pe = Column(Numeric(10, 2))
    forward_eps = Column(Numeric(10, 2))
    dividend_yield = Column(Numeric(10, 2))
    ma50 = Column(Numeric(10, 2))
    ma200 = Column(Numeric(10, 2))
    profit_margins = Column(Numeric(10, 2))
    operating_margins = Column(Numeric(10, 2))
    ebitda = Column(Numeric(10, 0))
    shares_outstanding = Column(Numeric(10, 0))
    shortName = Column(String, index=True)
    r_on_assets = Column(Numeric(10, 2))
    r_on_equity = Column(Numeric(10, 2))
    total_revenue = Column(Numeric(10, 0))
    debt_to_equity = Column(Numeric(10, 2))

print('Lol oya do am if he easy ')