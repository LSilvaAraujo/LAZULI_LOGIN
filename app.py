import stripe
from flask import Flask, render_template, request, redirect, session, url_for
from Functions.StripeManager import StripeManager
from flask_mail import Mail, Message
from db.QueryManager import QueryManager
from Functions.ValidationManager import ValidationManager
from config import SECRET_KEY, MAIL_KEY, STRIPE_KEY
import db.setup

app = Flask(__name__)
app.secret_key = SECRET_KEY

stripe.api_key = STRIPE_KEY

product_manager = StripeManager()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'atendimentocliente.lazuli@gmail.com'
app.config['MAIL_PASSWORD'] = MAIL_KEY

mail = Mail(app)


@app.route('/home')
def home_page():
    if len(session) != 0:
        return render_template("home/home.html")
    return redirect("/")


@app.route('/home', methods=['POST'])
def fale_conosco():
    if len(session) != 0:
        query_manager = QueryManager()

        userData = query_manager.get_user_data(session['username'])

        msg = Message('Suporte Lazuli', sender=app.config['MAIL_USERNAME'], recipients=[userData[1]])
        msg.body = "Caro(a) {}, gostaria de ressaltar a importância do seu contato a nós, ao permanecer " \
                   "fiel a nossos serviços. Queremos proporcionar um atendimento de qualidade e que possa " \
                   "proporcionar uma experiência agradável a todos nossos clientes. Espero que tenha um ótimo dia e " \
                   "que possa continuar nos ajudando com seu apoio." \
                   "'Lazuli: Do geek para a cultura.'".format(userData[0])

        mail.send(msg)

    return redirect("/home")


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


@app.route('/new_user')
def show_signup():
    return render_template("new_user/user.html")


@app.route('/new_user', methods=['POST'])
def signup():
    fields = ['new-name', 'new-user', 'email', 'password', 'repeat-password']
    user_data = {}
    for field in fields:
        if field == 'email':
            user_data[field] = request.form.get(field).lower()
        else:
            user_data[field] = request.form.get(field)

    validation_manager = ValidationManager(user_data)
    valid = validation_manager.all_valid()

    if valid:
        manager = QueryManager()
        manager.register_user(user_data)
        return redirect('/')
    else:
        return show_signup()


@app.route('/perfil/perfil.html')
def show_profile():
    if len(session) != 0:
        return render_template('perfil/perfil.html')

    return redirect('/')


@app.route('/pedidos/pedidos.html')
def show_orders():
    if len(session) != 0:
        return render_template('pedidos/pedidos.html')

    return redirect('/')


@app.route('/addresses/addresses.html')
def show_addresses():
    if len(session) != 0:
        return render_template('addresses/addresses.html')

    return redirect('/')


@app.route('/addresses/new-address.html', methods=['POST'])
def add_address():
    query_manager = QueryManager()
    if len(session) != 0:
        data = {'nome': request.form.get('nome'), 'email': request.form.get('email'), 'cpf': request.form.get('cpf'),
                'endereco': request.form.get('endereco'), 'pais': request.form.get('country'),
                'cep': request.form.get('cep'), 'telefone': request.form.get('phone'), 'username': session['username']}

        query_manager.register_address(data)

        return redirect('/addresses/addresses.html')


@app.route('/addresses/new-address.html')
def show_add_address():
    if len(session) != 0:
        return render_template('addresses/new-address.html')


@app.route('/checkout/<string:stripe_id>', methods=['POST'])
def checkout(stripe_id):
    price = stripe.Price.list(product=stripe_id)["data"][0]["id"]

    checkoutSession = stripe.checkout.Session.create(
        success_url=url_for('success', stripe_id=stripe_id, _external=True),
        cancel_url=url_for('cancel', _external=True),
        payment_method_types=['card'],
        line_items=[
            {
                'price': price,
                'quantity': 1
            }
        ],
        mode='payment'
    )

    print(checkoutSession.url)

    return redirect(checkoutSession.url)


@app.route('/success/<string:stripe_id>')
def success(stripe_id):
    if len(session) != 0:
        redirect('/')
    query_manager = QueryManager()
    query_manager.register_order(query_manager.get_id_user(session['username']), stripe_id)

    return redirect('/perfil/perfil.html')


@app.route('/view_products')
def view_productss():
    return render_template('req.html')


@app.route('/cancel')
def cancel():
    if len(session) != 0:
        redirect('/')
    return redirect('/perfil/perfil.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run()
