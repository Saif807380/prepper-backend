from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from .db import Base

plans_cities_table = Table('plans_cities', Base.metadata,
    Column('plan_id', Integer, ForeignKey('travel_plans.id')),
    Column('city_id', Integer, ForeignKey('cities.id'))
)

plans_pills_table = Table('plans_pills', Base.metadata,
    Column('plan_id', Integer, ForeignKey('travel_plans.id')),
    Column('pill_id', Integer, ForeignKey('pills.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    password = Column(String)

    plans = relationship("TravelPlan", lazy='joined')

class TravelPlan(Base):
    __tablename__ = "travel_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    start_date = Column(Date)
    end_date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))

    cities = relationship('City', secondary=plans_cities_table, back_populates="plans", lazy='joined')
    pills = relationship('Pill', secondary=plans_pills_table, back_populates="plans", lazy='joined')

class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    duration = Column(Integer)

    plans = relationship('TravelPlan', secondary=plans_cities_table, back_populates="cities", lazy='joined')

class Pill(Base):
    __tablename__ = "pills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    dosage = Column(Integer)
    stock = Column(Integer)
    time = Column(Integer)
    period = Column(String)
    plans = relationship('TravelPlan', secondary=plans_pills_table, back_populates="pills", lazy='joined')
