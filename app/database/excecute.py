from .connection import get_db_connection
import psycopg2.extras

def execute_query(query, params=None, fetchone=True):
    conn = get_db_connection()
    if conn is None:
        raise RuntimeError("Database connection failed")

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query, params)

            if query.strip().lower().startswith("select") or "returning" in query.lower():
                return cursor.fetchone() if fetchone else cursor.fetchall()

            conn.commit()
            return None

    except Exception as e:
        conn.rollback()
        raise

    finally:
        conn.close()
