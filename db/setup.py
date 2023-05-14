import sqlite3

# Connect to or create the SQLite database file
conn = sqlite3.connect('lazuli.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table for users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL
        
    )
''')

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()
