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
    CREATE TABLE IF NOT EXISTS enderecos (
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
    CREATE TABLE IF NOT EXISTS user_endereco (
        id_usuario INTEGER,
        id_endereco INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES users (id),
        FOREIGN KEY (id_endereco) REFERENCES enderecos (id)
    )
''')
conn.commit()


# Create the inventory table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventario (
        id_produto TEXT PRIMARY KEY,
        estoque INTEGER
    )
''')
conn.commit()

conn.close()