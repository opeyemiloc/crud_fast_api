import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


def _get_pg_creds():
    return {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "DB_NAME": os.getenv("DB_NAME"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    }


def start_pg_connection():

    try:
            creds = _get_pg_creds()

            connection = psycopg2.connect(
            host=creds["DB_HOST"],
            port=creds["DB_PORT"],
            dbname=creds["DB_NAME"],
            user=creds["DB_USER"],
            password=creds["DB_PASSWORD"])
            
            return connection
    except Exception as error:
         print("connection to database failed")
         print("Error : ", error)


def query_db(connection,query_str):
    conn = connection
    cursor = conn.cursor()
    cursor.execute(query_str)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows