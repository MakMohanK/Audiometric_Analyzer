# app.py

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'mohan_kshirsagar'

# SQLite3 database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the database if not exists
def init_db():
    conn = get_db_connection()
    with app.open_resource('schema.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()

# Initialize the database
try:
    init_db()
except sqlite3.OperationalError:
    pass  # Database already exists

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        f_name = request.form['first_name']
        l_name = request.form['last_name']
        gender = request.form['gender']
        age = request.form['age']
        dob = request.form['dob']
        mobile = request.form['mobile_number']


        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the email already exists
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already exists. Please choose a different one.', 'error')
        else:
            cursor.execute('INSERT INTO users (email, password, first_name, last_name, gender, age, dob, mobile_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (email, password, f_name, l_name, gender, age, dob, mobile))
            conn.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

        conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['email'] = email
            return redirect(url_for('profile'))
        else:
            flash('Login failed. Please check your email and password.', 'error')

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'email' in session:
        email = session['email']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        conn.close()

        if user:
            return render_template('profile.html', user=user)
        else:
            flash('User not found.', 'error')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
