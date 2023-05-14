from flask import Flask, render_template, request
from db.QueryManager import QueryManager

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template("home/home.html")


@app.route('/login')
def show_login():
    return render_template("login/login.html")


@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('user')
    password = request.form.get('password')
    manager = QueryManager()
    valid = manager.valid_credentials(user, password)
    manager.cursor.close()
    return {"valid": valid}  # para propósitos de teste
    # TODO: implementação hash & salt para senhas armazenadas no banco de dados


if __name__ == '__main__':
    app.run()
