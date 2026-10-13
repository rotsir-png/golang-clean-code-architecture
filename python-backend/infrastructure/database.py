import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg.connect(
        host="localhost",
        dbname="khaojai_db",
        user="postgres",
        password=os.environ["KHAOJAI_DB_PASSWORD"]
    )