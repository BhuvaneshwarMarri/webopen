import webbrowser
import argparse
import click
import sqlite3

def create_db():
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS creds(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def main():
    def open_link(website):
        webbrowser.open(f"http://{website}")

    def add_data(website, username, password):
        try:
            conn = sqlite3.connect('credentials.db')
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO creds (website, username, password) VALUES (?, ?, ?)
            ''', (website, username, password))
            conn.commit()
            click.echo("Data is added successfully.")
        except sqlite3.Error as e:
            click.echo(f"An error occurred: {e}")
        finally:
            conn.close()

    def search_data(website):
        try:
            conn = sqlite3.connect('credentials.db')
            cursor = conn.cursor()
            cursor.execute('''
            SELECT website, username, password
            FROM creds
            WHERE website=?
            ''', (website,))
            data = cursor.fetchone()
            if data:
                labels = ["Website", "Username", "Password"]
                for i in range(3):
                    click.echo(f"{labels[i]} : {data[i]}")
            else:
                click.echo("No data found for the specified website.")
        except sqlite3.Error as e:
            click.echo(f"An error occurred: {e}")
        finally:
            conn.close()
        
    def credential_add():
        website = click.prompt("Enter website name")
        username = click.prompt("Enter username for website")
        password = click.prompt("Enter password for website")
        add_data(website, username, password)
    
    def credential_search():
        website = click.prompt("Enter website name to search")
        search_data(website)
        
    parser = argparse.ArgumentParser(description="Manage credentials and open links.")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    parser.add_argument("-link", dest="link_name", help="The name of the link to open")
    subparsers.add_parser("add", help="Add a new credential")
    subparsers.add_parser("search", help="Search for a credential")
    args = parser.parse_args()
    
    if args.link_name:
        open_link(args.link_name)
    elif args.command == "add":
        credential_add()
    elif args.command == "search":
        credential_search()
    else:
        parser.print_help()

if __name__ == "__main__":
    create_db()
    main()
