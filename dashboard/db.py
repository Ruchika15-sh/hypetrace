from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
host = os.getenv("DB_HOST")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql://{user}:{password}@{host}/{dbname}?sslmode=require")