import sqlite3
from Functions.HashingManager import HashingManager


class QueryManager:
    def __init__(self):
        self.conn = sqlite3.connect("db/lazuli.db")
        self.cursor = self.conn.cursor()

    def close_connections(self):
        self.cursor.close()
        self.conn.close()

    def valid_credentials(self, username, password):
        self.cursor.execute('SELECT senha FROM users WHERE username = ?',
                            (username,))
        result = self.cursor.fetchone()
        if result is None:
            return False
        valid = HashingManager.is_valid_password(password, result[0])
        self.close_connections()
        return valid

    def exists_value(self, table, field, value):
        query = 'SELECT * FROM {} WHERE {} = ?'.format(table, field)
        self.cursor.execute(query, (value,))
        result = self.cursor.fetchone()
        self.close_connections()
        return result is not None

    def register_user(self, data):
        password = data['password']
        hashing_manager = HashingManager(password)
        hash_data = hashing_manager.get_data()
        data['password'] = hash_data['password']

        self.cursor.execute('INSERT INTO users (username, nome, email, senha) '
                            'VALUES (?,?,?,?)',
                            (data['new-user'], data['new-name'], data['email'],
                             data['password']))
        self.conn.commit()
        self.close_connections()

        # INSERT INTO people (first_name, last_name) VALUES ("John", "Smith");
        # ['new-name', 'new-user', 'email', 'password', 'repeat-password']

    def get_password(self, username):
        self.cursor.execute('SELECT senha FROM users WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        self.close_connections()
        return result

    def get_contact(self, username):
        self.cursor.execute('SELECT username, nome, email FROM users WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        self.close_connections()
        return result

    def register_product(self, data):
        self.cursor.execute('INSERT INTO produtos (id_produto, estoque, nome, descricao) '
                            'VALUES (?,?,?,?)',
                            (data['id_produto'], data['estoque'], data['nome'],
                             data['descricao']))
        self.conn.commit()
        self.close_connections()
