import sqlite3
from Functions.HashingManager import HashingManager


class QueryManager:
    def __init__(self):
        self.conn = sqlite3.connect("db/lazuli.db")
        self.cursor = self.conn.cursor()

    def valid_credentials(self, username, password):
        self.cursor.execute('SELECT senha FROM users WHERE user = ?',
                            (username,))
        result = self.cursor.fetchone()[0]
        print(password, result[0])
        if result is None:
            return False
        valid = HashingManager.is_valid_password(password, result)
        self.cursor.close()
        self.conn.close()
        return valid

    def exists_username(self, username):
        self.cursor.execute('SELECT * FROM users WHERE user = ?', (username,))
        result = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return result is not None

    def exists_email(self, email):
        self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        result = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return result is not None

    def register_user(self, data):
        password = data['password']
        hashing_manager = HashingManager(password)
        hash_data = hashing_manager.get_data()
        data['password'] = hash_data['password']

        self.cursor.execute('INSERT INTO users (user, nome, email, senha) '
                            'VALUES (?,?,?,?)',
                            (data['new-user'], data['new-name'], data['email'],
                             data['password']))
        self.conn.commit()
        self.cursor.close()

        # INSERT INTO people (first_name, last_name) VALUES ("John", "Smith");
        # ['new-name', 'new-user', 'email', 'password', 'repeat-password']

    def get_password(self, username):
        self.cursor.execute('SELECT senha FROM users WHERE user = ?', (username,))
        result = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return result
