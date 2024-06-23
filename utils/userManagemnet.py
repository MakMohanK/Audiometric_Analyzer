import sqlite3
from getpass import getpass
import hashlib

USER_MANAGEMNET_DATABASE = './database/user_management.db'

# Function to create the database and the users table
def create_database():
    conn = sqlite3.connect(USER_MANAGEMNET_DATABASE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    userfullname,
                    usergender,
                    userage,
                    userdob)''')
    conn.commit()
    conn.close()

# Function to register a new user
def register_user():
    username = input("Enter a username: ")
    password = getpass("Enter a password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect(USER_MANAGEMNET_DATABASE)
    cur = conn.cursor()
    
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Error: Username already exists!")
    
    conn.close()

# Function to login a user
def login_user():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect(USER_MANAGEMNET_DATABASE)
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password_hash))
    user = cur.fetchone()
    
    conn.close()
    
    if user:
        print(user)
        print("Login successful!")
    else:
        print("Error: Invalid username or password!")

# Main function to display the menu
def main():
    create_database()
    
    while True:
        print("\nUser Management System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()



