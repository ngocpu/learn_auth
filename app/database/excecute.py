from .connection import get_db_connection

def execute_query(query, params=None):
    conn = get_db_connection()
    if conn is None:
        return {"error": "Database connection failed"}

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            conn.commit()
            return {"message": "Query executed successfully"}
    except Exception as e:
        print(f"Error executing query: {e}")
        return {"error": str(e)}
    finally:
        conn.close()
