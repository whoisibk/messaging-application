import psycopg2
from sqlalchemy import create_engine
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

connection = engine.connect()
