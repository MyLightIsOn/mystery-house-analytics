import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')

def create_table():
    if not DATABASE_URL:
        print("DATABASE_URL not found in environment variables.")
        return

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS puzzle_logs (
                id SERIAL PRIMARY KEY,
                session_id TEXT NOT NULL,
                puzzle_id TEXT NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                duration_seconds INTEGER NOT NULL,
                attempt_number INTEGER NOT NULL
            );
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("Table 'puzzle_logs' created or already exists.")

    except Exception as e:
        print("Failed to create table:", e)

if __name__ == "__main__":
    create_table()
