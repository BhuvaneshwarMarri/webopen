import sqlite3
from webopen.db.config import DATABASE_URL
from webopen.db.connection import get_db

def create_tables():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS creds (
            id INTEGER PRIMARY KEY,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        conn.commit()
