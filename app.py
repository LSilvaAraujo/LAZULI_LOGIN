from flask import Flask, render_template, request, redirect
from db.QueryManager import QueryManager
from Functions.ValidationManager import ValidationManager

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
    query_manager = QueryManager()
    valid = query_manager.valid_credentials(user, password)
    if valid:
        return {"valid": valid}  # para propósitos de teste
    else:
        return show_login()
    # TODO: implementação hash & salt para senhas armazenadas no banco de dados


@app.route('/new_user/user.html')
def show_signup():
    return render_template("new_user/user.html")


@app.route('/new_user/user.html', methods=['POST'])
def signup():
    fields = ['new-name', 'new-user', 'email', 'password', 'repeat-password']
    user_data = {}
    for field in fields:
        user_data[field] = request.form.get(field)

    validation_manager = ValidationManager(user_data)
    valid = validation_manager.all_valid()

    if valid:
        manager = QueryManager()
        manager.register_user(user_data)
        return redirect('/login')
    else:
        return show_signup()


if __name__ == '__main__':
    app.run()
