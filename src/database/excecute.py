import psycopg2.extras

def execute_query(query, params=None, fetchone=True, conn=None):
    if conn is None:
        raise ValueError("Connection must be provided")

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute(query, params)

        if query.strip().lower().startswith("select") or "returning" in query.lower():
            return cursor.fetchone() if fetchone else cursor.fetchall()

        conn.commit()
        return None
