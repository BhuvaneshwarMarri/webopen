import argparse
import sqlite3
import getpass
import time
import hashlib
import os
from datetime import datetime, timedelta

class AuthCLI:
    def __init__(self, db_name='./users.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        self.session_duration = timedelta(hours=1)
        self.last_auth_time = None

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
        (username TEXT PRIMARY KEY, password TEXT)
        ''')
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password):
        cursor = self.conn.cursor()
        hashed_password = self.hash_password(password)
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (username, hashed_password))
            self.conn.commit()
            print("User created successfully.")
        except sqlite3.IntegrityError:
            print("Username already exists.")

    def authenticate(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result and result[0] == self.hash_password(password):
            self.last_auth_time = datetime.now()
            return True
        return False

    def check_session(self):
        if not self.last_auth_time:
            return False
        return datetime.now() - self.last_auth_time < self.session_duration

    def run(self):
        parser = argparse.ArgumentParser(description="CLI Application with Authentication")
        parser.add_argument("--user", help="Username for authentication")
        parser.add_argument("--password", help="Password for authentication")
        args = parser.parse_args()

        if args.user and args.password:
            if self.authenticate(args.user, args.password):
                print("Authentication successful.")
                self.main_functionality()
            else:
                print("Authentication failed.")
        else:
            self.interactive_mode()

    def interactive_mode(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            print("No users found. Please create an account.")
            username = input("Enter a username: ")
            password = getpass.getpass("Enter a password: ")
            self.create_user(username, password)

        while True:
            try:
                if not self.check_session():
                    username = input("Enter your username: ")
                    password = getpass.getpass("Enter your password: ")
                    if self.authenticate(username, password):
                        print("Authentication successful.")
                        self.main_functionality()
                    else:
                        print("Authentication failed.")
                else:
                    self.main_functionality()
            except KeyboardInterrupt:
                print("\nExiting the application. Goodbye!")
                break

    def main_functionality(self):
        print("\nWelcome to the Note-Taking CLI application!")
        print(f"Your session will expire in {self.session_duration.seconds // 3600} hour(s).")
        
        while True:
            print("\nMain Menu:")
            print("1. Save a new note")
            print("2. View saved notes")
            print("3. Logout")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == '1':
                self.save_note()
            elif choice == '2':
                self.view_notes()
            elif choice == '3':
                print("Logging out...")
                self.last_auth_time = None
                break
            else:
                print("Invalid choice. Please try again.")

    def save_note(self):
        note = input("Enter your note: ")
        while True:
            save_path = input("Enter the path to save the note (including filename): ")
            save_path = os.path.expanduser(save_path)  # Expand user directory if used

            # Check if the directory exists
            dir_path = os.path.dirname(save_path)
            if not os.path.exists(dir_path):
                create_dir = input(f"Directory {dir_path} doesn't exist. Create it? (y/n): ")
                if create_dir.lower() == 'y':
                    os.makedirs(dir_path)
                else:
                    continue

            # Check if the file already exists
            if os.path.exists(save_path):
                overwrite = input("File already exists. Overwrite? (y/n): ")
                if overwrite.lower() != 'y':
                    continue

            # If we've made it here, we can save the file
            with open(save_path, 'w') as file:
                file.write(note)
            print(f"Note saved successfully to {save_path}")
            break

    def view_notes(self):
        notes_dir = input("Enter the directory path to view notes: ")
        notes_dir = os.path.expanduser(notes_dir)  # Expand user directory if used
        if not os.path.exists(notes_dir):
            print(f"Directory {notes_dir} doesn't exist.")
            return
        
        notes = [f for f in os.listdir(notes_dir) if f.endswith('.txt')]
        if not notes:
            print("No notes found in the specified directory.")
            return
        
        print("\nAvailable notes:")
        for i, note in enumerate(notes, 1):
            print(f"{i}. {note}")
        
        choice = input("\nEnter the number of the note to view (or 'q' to go back): ")
        if choice.lower() == 'q':
            return
        
        try:
            note_index = int(choice) - 1
            if 0 <= note_index < len(notes):
                with open(os.path.join(notes_dir, notes[note_index]), 'r') as file:
                    print(f"\nContents of {notes[note_index]}:")
                    print(file.read())
            else:
                print("Invalid note number.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")

if __name__ == "__main__":
    cli = AuthCLI()
    cli.run()