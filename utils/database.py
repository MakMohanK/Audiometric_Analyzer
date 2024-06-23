import sqlite3

# Create a connection to a new SQLite database (or connect to an existing one)
conn = sqlite3.connect('example.db')

# Create a cursor object
cur = conn.cursor()

# Execute a simple SQL command
cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')

# Commit the changes
conn.commit()

# Close the connection
conn.close()
