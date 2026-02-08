from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
   __tablename__ = "users"

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, nullable=False)
   average_spending = Column(Numeric(10, 2), default=0.00)