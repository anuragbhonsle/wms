import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv(override=True)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )


def fetch_all(query):
    connection = get_db_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()


print("Connecting to:", os.getenv("DB_HOST"))