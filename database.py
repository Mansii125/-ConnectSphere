# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    culture_tags = Column(Text)

class PGListing(Base):
    __tablename__ = 'pg_listings'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    rent = Column(Float)
    tags = Column(Text)

class FoodPlace(Base):
    __tablename__ = 'food_places'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    cuisine = Column(String)
    tags = Column(Text)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    type = Column(String)
    tags = Column(Text)

class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    item_id = Column(Integer)
    item_type = Column(String)  # pg/food/event

# --- Create DB ---
engine = create_engine('sqlite:///connectsphere.db')
Session = sessionmaker(bind=engine)
session = Session()

def create_tables():
    Base.metadata.create_all(engine)

