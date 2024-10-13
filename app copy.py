# app.py (part of the code)

import datetime
import sqlite3

# Ensure the database has the necessary column
def init_db():
    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,        -- Adding first name
        last_name TEXT NOT NULL,         -- Adding last name
        mobile_number TEXT NOT NULL,     -- Adding mobile number
        role TEXT NOT NULL               -- Adding role Doctor or patient
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analysis_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        age INTEGER NOT NULL,
        timestamp DATETIME NOT NULL,
        response TEXT NOT NULL,                        -- Adding results
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    conn.commit()
    conn.close()

init_db()


# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('auth.db')
    conn.row_factory = sqlite3.Row
    return conn


def play_sound():
    frequency = request.args.get('frequency')
    decibel = request.args.get('decibel')
    # Generate or play the sound (This is a placeholder; you would use a sound generation library)
    return f"Playing sound at {frequency} Hz and {decibel} dB"

# Route to handle response submission
@app.route('/submit_response', methods=['POST'])
def submit_response():
    data = request.get_json()
    dob = data.get('dob')
    responses = data.get('responses')
    status = data.get('status')

    # Calculate age
    birth_date = datetime.strptime(dob, '%Y-%m-%d')
    age = (datetime.now() - birth_date).days // 365

    # Store responses in database (or for now, just print them)
    print(f"User Age: {age}")
    print(f"Test Status: {status}")
    print("User Responses:", responses)

    # Here, you'd add code to store the responses in a database, including the timestamp

    # Example response
    return jsonify({"message": "Response recorded!", "status": status})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        mobile_number = request.form['mobile_number']
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password, first_name, last_name, mobile_number, role) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',(username, email, password, first_name, last_name, mobile_number, role))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Username or email already exists')
            return redirect(url_for('register'))
        finally:
            conn.close()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/change_password')
def change_password():
    return render_template('change_password.html')

@app.route('/audiometric_test')
def audiometric_test():
    return render_template('audiometric_test.html')

@app.route('/recognition_test')
def recognition_test():
    return render_template('recognition_test.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['first_name'] = user['first_name'][0].upper()+user['first_name'][1:]
            session['last_name'] = user['last_name'][0].upper()+user['last_name'][1:]
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch user by email
        cursor.execute('SELECT * FROM users WHERE email = ? AND username = ?', (email, username))
        user = cursor.fetchone()

        if user:
            # If user exists, update their password to 'Sunday@123'
            default_password = 'Sunday@123'
            hashed_password = generate_password_hash(default_password)  # Hash the default password for security
            
            # Update the password in the database
            cursor.execute('UPDATE users SET password = ? WHERE email = ?', (hashed_password, email))
            conn.commit()

            # Notify the user about the reset
            flash(f'Password has been reset to "{default_password}". Please change it after logging in.')

            # Optionally, you can redirect the user to the login page
            return redirect(url_for('login'))
        else:
            # If email not found, flash an error message
            flash('Email not found.')

        conn.close()

    return render_template('forgot_password.html')

@app.route('/analysis')
def analysis():
    if 'user_id' not in session:
        flash('You need to log in first.')
        return redirect(url_for('login'))
    return render_template('analysis.html')

@app.route('/save_analysis', methods=['POST'])
def save_analysis():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    heard_sound = data.get('heard')
    frequency = data.get('frequency')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analysis_results (user_id, heard_sound, frequency)
        VALUES (?, ?, ?)
    ''', (session['user_id'], heard_sound, frequency))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
