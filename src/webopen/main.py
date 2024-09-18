import webbrowser
import argparse
from webopen.db.connection import get_db
from webopen.db.models import create_tables
import click
from datetime import datetime
from authentication import verify_user
import random
import string
import pyperclip

def gen_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for i in range(length))
    pyperclip.copy(password)
    print("Password is successfully generated and copied to your clip board, Use ctrl+V or Win+V to verify")

def add_data(website, username, password):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO creds (website,username,password) VALUES (?,?,?)', (website, username, password,))
        conn.commit()
        click.echo("Data added successfully")

def credential_add():
    create_tables()
    website = click.prompt("Enter website name")
    username = click.prompt("Enter username for website")
    password = click.prompt("Enter password for website")
    add_data(website, username, password)

def search_data(website):
    create_tables()
    with get_db() as conn:
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
            return True
        else:
            click.echo("No data found for the specified website.")
            return False

def credential_search():
    website = click.prompt("Enter website name to search")
    search_data(website)

def delete_data(website):
    create_tables()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        DELETE FROM creds
        WHERE website=?
        ''', (website,))
        conn.commit()
        click.echo("Data deleted successfully")

def credential_delete():
    website = click.prompt("Enter website name to delete")
    x=search_data(website)
    if x:
        choice = click.prompt("Enter yes to delete this credential else type no")
        if choice == "yes":
            delete_data(website)
        else:
            click.echo("Successfully exited from delete process")
    
def open_link(website):
    webbrowser.open(f"http://{website}")
        
def main():
    
    parser = argparse.ArgumentParser(description="Manage credentials and open links.")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    parser.add_argument("-link", dest="link_name", help="The name of the link to open")
    subparsers.add_parser("add", help="Add a new credential")
    subparsers.add_parser("search", help="Search for a credential")
    subparsers.add_parser("delete",help="Delete a particular credential")
    subparsers.add_parser("generate",help="Help to generate password directly copied to your clip board")
    args = parser.parse_args()
    
    if args.link_name:
        open_link(args.link_name)
    elif verify_user():
        if args.command == "add":
            credential_add()
        elif args.command == "search":
            credential_search()
        elif args.command == "delete":
            credential_delete()
        elif args.command == "generate":
            gen_password()
        else:
            parser.print_help()

if __name__ == "__main__":
    create_tables()
    main()
