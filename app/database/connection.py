import psycopg2
from app.core import settings
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            port=settings.DB_PORT
        )
        print("Database connection established")
        return conn
    except Exception as e:
        print(f"Error establishing database connection: {e}")
        return None 

