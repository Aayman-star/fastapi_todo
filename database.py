import os
from sqlalchemy import create_engine, Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv,find_dotenv

"""Loading the environment variable"""
load_dotenv(find_dotenv())

DATABASE_URL = os.environ["DATABASE_URL"]
print(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    is_complete = Column(Boolean, default=False) 

class UserList(Base):  
    __tablename__ = "users"  

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True)  
    useremail=Column(String,unique=True)
    hashed_password=Column(String)


Base.metadata.create_all(engine)
