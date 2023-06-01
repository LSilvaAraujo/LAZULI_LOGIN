import sqlite3

# Connect to or create the SQLite database file
conn = sqlite3.connect('db/lazuli.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

cursor.execute('''
PRAGMA foreign_keys = ON
''')

# Create a table for users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL
    )
''')

# Create a table for addresses
cursor.execute('''
    CREATE TABLE IF NOT EXISTS enderecos (
        id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        cpf TEXT NOT NULL,
        endereco TEXT NOT NULL,
        pais TEXT NOT NULL,
        cep TEXT NOT NULL,
        telefone TEXT NOT NULL
    )
''')

# Create a table for user_address relationship
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_endereco (
        id_usuario_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario_fk INTEGER,
        id_endereco_fk INTEGER,
        FOREIGN KEY (id_usuario_fk) REFERENCES users (id_user),
        FOREIGN KEY (id_endereco_fk) REFERENCES enderecos (id_endereco)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user_fk,
        id_endereco_fk,
        id_produto_fk,
        FOREIGN KEY (id_user_fk) REFERENCES users (id_user),
        FOREIGN KEY (id_endereco_fk) REFERENCES enderecos (id_endereco),
        FOREIGN KEY (id_produto_fk) REFERENCES produtos (id_produto)
    )
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos(
id_produto TEXT NOT NULL PRIMARY KEY,
estoque INTEGER NOT NULL,
nome TEXT NOT NULL,
descricao TEXT NOT NULL)
''')

conn.commit()

conn.close()
