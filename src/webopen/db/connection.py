import sqlite3
from contextlib import contextmanager
from webopen.db.config import DATABASE_URL

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()
