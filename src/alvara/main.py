import flask
from flask import Flask, render_template, request
import os
from logic.account import account

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'static')
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    success = None
    if request.method == 'POST':
        try:
            fname = request.form['fname']
            lname = request.form['lname']
            age = int(request.form['age'])
            address = request.form['address']
            password = request.form['password']
            phone = request.form['phone']
            email = request.form['email']

            # Ne pas créer de carte à l'inscription
            account(fname, lname, age, address, password, phone, email, cards=[])
            success = "Account created successfully!"
        except Exception as e:
            error = str(e)
    return render_template('register.html', error=error, success=success)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    success = None
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            # Vérifier les informations d'identification de l'utilisateur
            account.login(email, password)
            success = "Login successful!"
        except Exception as e:
            error = str(e)
    return render_template('login.html', error=error, success=success)

if __name__ == '__main__':
    app.run(debug=False, port=5001)