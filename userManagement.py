import sqlite3
from getpass import getpass
import hashlib
from examineHearing import playAllFrequencies

USER_MANAGEMENT_DATABASE = './database/user_management.db'
logged_in = False
current_username = ""

def create_database():
    conn = sqlite3.connect(USER_MANAGEMENT_DATABASE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    userfullname,
                    usergender,
                    userage,
                    useremail,
                    userphoneno)''')
    conn.commit()
    conn.close()

def register():
    username = input("Enter a username: ")
    password = getpass("Enter a password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect(USER_MANAGEMENT_DATABASE)
    cur = conn.cursor()
    
    try:
        name = input("Enter your full name: ")
        gender = input("Enter your gender? M or F: ")
        age = input("Enter your age: ")
        email = input("Enter your email: ")
        phoneNumber = input("Enter your phone number: ")
        cur.execute("INSERT INTO users (username, password, userfullname, usergender, userage, useremail, userphoneno) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, password_hash, name, gender, age, email, phoneNumber))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Error: Username already exists!")
    
    conn.close()

def login():
    username = input("Enter your username: ")
    current_username = username
    password = getpass("Enter your password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect(USER_MANAGEMENT_DATABASE)
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password_hash))
    user = cur.fetchone()
    
    conn.close()
    
    if user:
        print(user)
        print("Login successful!")
        logged_in = True
    else:
        print("Error: Invalid username or password!")
        logged_in = False

def main():
    create_database()
    
    while True:
        if logged_in == False:
            print("\nUser Management System")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
        
            choice = input("Enter your choice: ")
            
            if choice == '1':
                register()
            elif choice == '2':
                login()
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            playAllFrequencies(current_username)

if __name__ == '__main__':
    main()