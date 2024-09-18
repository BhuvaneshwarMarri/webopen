from datetime import datetime, timedelta
import bcrypt
import webbrowser
import argparse
from webopen.db.connection import get_db
import click
from datetime import datetime

def create_tables():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS authentication (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at REAL NOT NULL
        )
        ''')
        conn.commit()
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def Signup_user():
    print("Greetings! Welcome to Webopen, hope you enjoy well")
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")
    hashed_password = hash_password(password)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO authentication (username, password, created_at)
        VALUES (?, ?, ?)
        """, (username, hashed_password, datetime.now().timestamp()))
        conn.commit()
    print("User created successfully!")

def Login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM authentication WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        if user_data and verify_password(user_data[1], password):
            print("Login successful!")
            cursor.execute("UPDATE authentication SET created_at = ? WHERE username = ?", 
                           (datetime.now().timestamp(), username))
            conn.commit()
            return True
        else:
            print("Invalid username or password.")
            return False

def verify_user():
    create_tables()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, created_at FROM authentication")
        data = cursor.fetchone()
        if not data:
            Signup_user()
            return True
        else:
            last_login_time = datetime.fromtimestamp(data[2])
            if datetime.now() - last_login_time > timedelta(minutes=20):
                # print("Hello")
                return Login_user()
            else:
                return True

# if __name__ == "__main__":
#     create_tables()
#     verify_user()