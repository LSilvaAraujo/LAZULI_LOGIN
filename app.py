from flask import Flask, render_template, request, redirect, session
from db.QueryManager import QueryManager
from Functions.ValidationManager import ValidationManager
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/home')
def home_page():
    if len(session) != 0:
        return render_template("home/home.html")
    return redirect("/")


@app.route('/')
def show_login():
    return render_template("login/login.html")


@app.route('/', methods=['POST'])
def login():
    user = request.form.get('user')
    password = request.form.get('password')
    query_manager = QueryManager()
    valid = query_manager.valid_credentials(user, password)
    if valid:
        session['username'] = user
        return redirect('/home')
    else:
        return show_login()
    # TODO: implementação hash & salt para senhas armazenadas no banco de dados


@app.route('/new_user')
def show_signup():
    return render_template("new_user/user.html")


@app.route('/new_user', methods=['POST'])
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
        return redirect('/')
    else:
        return show_signup()


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run()
