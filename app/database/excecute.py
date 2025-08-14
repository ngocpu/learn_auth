from .connection import get_db_connection
import psycopg2.extras

def execute_query(query, params=None, fetchone=True, conn=None):
    close_conn = False
    if conn is None:
        conn = get_db_connection()
        close_conn = True

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query, params)

            if query.strip().lower().startswith("select") or "returning" in query.lower():
                return cursor.fetchone() if fetchone else cursor.fetchall()

            if close_conn:
                conn.commit()
            return None

    except Exception as e:
        if close_conn:
            conn.rollback()
        raise

    finally:
        if close_conn:
            conn.close()
