from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
print("Looking for .env at:", os.path.abspath(".env"))
print("File exists:", os.path.exists(".env"))
password = os.getenv("DB_PASSWORD")
print("Password loaded:", repr(password)) 

host = os.getenv("DB_HOST")
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
engine = create_engine(f"postgresql://{user}:{password}@{host}/{dbname}?sslmode=require")

if __name__ == "__main__":
    with engine.connect() as conn:
        print("Connected successfully!")

       
