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
        cpf TEXT NOT NULL,
        senha TEXT NOT NULL
    )
''')
conn.commit()

# Create a table for addresses
cursor.execute('''
    CREATE TABLE IF NOT EXISTS addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        bairro TEXT NOT NULL,
        cidade TEXT NOT NULL,
        UF TEXT NOT NULL,
        cep TEXT NOT NULL,
        numero INTEGER NOT NULL,
        complemento TEXT NOT NULL
    )
''')
conn.commit()

# Create a table for user_address relationship
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_address (
        user_id INTEGER,
        address_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (address_id) REFERENCES addresses (id)
    )
''')
conn.commit()

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()
