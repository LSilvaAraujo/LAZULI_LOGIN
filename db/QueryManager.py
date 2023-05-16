import sqlite3


class QueryManager:
    def __init__(self):
        self.conn = sqlite3.connect("db/lazuli.db")
        self.cursor = self.conn.cursor()

    def valid_credentials(self, username, password):
        self.cursor.execute('SELECT * FROM users WHERE user = ? AND senha = ?',
                            (username, password))
        result = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return result is not None

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
        self.cursor.execute('INSERT INTO users (user, nome, email, senha) '
                            'VALUES (?,?,?,?)',
                            (data['new-name'], data['new-user'], data['email'],
                             data['password']))
        self.conn.commit()
        self.cursor.close()

        # INSERT INTO people (first_name, last_name) VALUES ("John", "Smith");
        # ['new-name', 'new-user', 'email', 'password', 'repeat-password']
