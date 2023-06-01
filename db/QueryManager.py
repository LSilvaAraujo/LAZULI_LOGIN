import sqlite3
from Functions.HashingManager import HashingManager


class QueryManager:
    def __init__(self):
        self.conn = sqlite3.connect("db/lazuli.db")
        self.cursor = self.conn.cursor()


    def valid_credentials(self, username, password):
        self.cursor.execute('SELECT senha FROM users WHERE username = ?',
                            (username,))
        result = self.cursor.fetchone()
        if result is None:
            return False
        valid = HashingManager.is_valid_password(password, result[0])
        return valid

    def exists_value(self, table, field, value):
        query = 'SELECT * FROM {} WHERE {} = ?'.format(table, field)
        self.cursor.execute(query, (value,))
        result = self.cursor.fetchone()
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


    def get_password(self, username):
        self.cursor.execute('SELECT senha FROM users WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        return result

    def get_user_data(self, username):
        self.cursor.execute('SELECT nome, email FROM users WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        return result

    def get_id_user(self, username):
        self.cursor.execute('SELECT id_user FROM users WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        return result

    def register_product(self, data):
        self.cursor.execute('INSERT INTO produtos (id_produto, estoque, nome, descricao) '
                            'VALUES (?,?,?,?)',
                            (data['id_produto'], data['estoque'], data['nome'],
                             data['descricao']))
        self.conn.commit()

    def register_address(self, data):
        self.cursor.execute('SELECT id_user FROM users WHERE username = ?', (data['username'],))
        id_user = self.cursor.fetchone()[0]

        # Check if the user already has an address
        self.cursor.execute('SELECT id_endereco_fk, id_usuario_endereco FROM user_endereco WHERE id_usuario_fk = ?',
                            (id_user,))
        existing_address = self.cursor.fetchone()

        if existing_address:
            id_endereco_fk, id_usuario_endereco = existing_address
            self.cursor.execute(
                'UPDATE enderecos SET nome = ?, email = ?, cpf = ?, endereco = ?, pais = ?, cep = ?, telefone = ? WHERE id_endereco = ?',
                (
                    data['nome'], data['email'], data['cpf'], data['endereco'], data['pais'], data['cep'],
                    data['telefone'],
                    id_endereco_fk))
            self.cursor.execute('UPDATE user_endereco SET id_endereco_fk = ? WHERE id_usuario_endereco = ?',
                                (id_endereco_fk, id_usuario_endereco))
        else:
            self.cursor.execute(
                'INSERT INTO enderecos (id_endereco, nome, email, cpf, endereco, pais, cep, telefone) VALUES (NULL,?,?,?,?,?,?,?)',
                (data['nome'], data['email'], data['cpf'], data['endereco'], data['pais'], data['cep'],
                 data['telefone']))
            id_endereco_fk = self.cursor.lastrowid
            self.cursor.execute(
                'INSERT INTO user_endereco (id_usuario_endereco, id_usuario_fk, id_endereco_fk) VALUES (NULL,?,?)',
                (id_user, id_endereco_fk))

        self.conn.commit()

    def register_order(self, id_user, id_produto):

        id_user = id_user[0]

        self.cursor.execute('''
            SELECT id_endereco_fk FROM user_endereco WHERE id_usuario_fk = ?''',
                            (id_user,))

        address_id = self.cursor.fetchone()[0]

        self.cursor.execute('''
            INSERT INTO pedidos (id_user_fk, id_endereco_fk, id_produto_fk)
            VALUES (?, ?, ?)
            ''', (id_user, address_id, id_produto))

        self.cursor.execute('''
                UPDATE produtos
                SET estoque = estoque - 1
                WHERE id_produto = ?
                ''', (id_produto,))

        self.conn.commit()
