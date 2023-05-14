import sqlite3


class QueryManager:
    def __init__(self):
        conn = sqlite3.connect("db/lazuli.db")
        self.cursor = conn.cursor()

    def valid_credentials(self, username, password):
        self.cursor.execute('SELECT * FROM users WHERE user = ? AND senha = ?',
                            (username, password))
        result = self.cursor.fetchone()
        return result is not None
