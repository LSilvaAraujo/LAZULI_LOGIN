import sqlite3

# Connect to or create the SQLite database file
conn = sqlite3.connect('db/lazuli.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

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
conn.commit()

# Create a table for addresses
cursor.execute('''
    CREATE TABLE IF NOT EXISTS enderecos (
        id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
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
        id_usuario_fk INTEGER,
        id_endereco_fk INTEGER,
        FOREIGN KEY (id_usuario_fk) REFERENCES users (id_user),
        FOREIGN KEY (id_endereco_fk) REFERENCES enderecos (id_endereco)
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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id_pedido TEXT PRIMARY KEY,
        id_user_fk,
        id_endereco_fk,
        id_produto_fk,
        uuid TEXT NOT NULL,
        FOREIGN KEY (id_user_fk) REFERENCES users (id_user),
        FOREIGN KEY (id_endereco_fk) REFERENCES enderecos (id_endereco),
        FOREIGN KEY (id_produto_fk) REFERENCES inventario (id_produto)
    )
''')

conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos_pedido(
produtos_pedido_id INTEGER PRIMARY KEY AUTOINCREMENT,
uuid_fk TEXT NOT NULL,
FOREIGN KEY (uuid_fk) REFERENCES pedidos (uuid)
)''')
conn.commit()

conn.close()
