import psycopg2
from sqlalchemy import create_engine
from models import Base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# establish connection to db
connection = engine.connect()

# create tables from predefined models
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


connection.close()
