from flask import Blueprint, render_template,request,flash,redirect,url_for
from flask_login import current_user, login_required, login_user, logout_user
from src import db, app
from src.models.user import User
from itsdangerous import URLSafeSerializer,URLSafeTimedSerializer
import requests
from requests.exceptions import HTTPError



user_blueprint = Blueprint('users', __name__,template_folder='../../templates')

def send_email(token,email):
    url= "https://api.mailgun.net/v3/sandbox172ed4b367ea4418b3ef4ee81fc88b7b.mai/messages"
    try:
        response = requests.post(url,
            auth=("api", app.config['API_EMAIL']),
            data=
            {"from": "Hello Duc <ducnpgt60935@fpt.edu.vn>",
                "to": [email],
                "subject": "Reset Password",
                "text": f"Go to http://localhost:5000/new_password/{token}"})

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')



@user_blueprint.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        user = User.query.filter_by(email= request.form['email']).first()
        if user:
            flash("email has already register")
            return redirect(url_for('register'))
        new_user = User(email = request.form['email'], username= request.form['username'])
        new_user.set_password(request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('user/register.html')
    return render_template('user/register.html')


@user_blueprint.route('/ticket/profile')
@login_required
def profile():
    
    return render_template('user/profile.html')


@user_blueprint.route('/', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash("success")
        return redirect(url_for('users.profile'))
    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            if user.check_password(request.form['password']):
                login_user(user)
                print("welcome {0}".format(user.email), 'success')
                return redirect(url_for('users.profile'))
        flash("email invalid")
        return redirect(url_for('users.login'))
    return render_template('user/login.html')




@user_blueprint.route('/forget-password', methods=['GET','POST'])
def forget():
    if current_user.is_authenticated:
        return redirect(url_for('users.root'))
    if request.method == "POST":
        user = User(email = request.form['email']).check_user()
        if not user:
            flash("Account not exist")
            return redirect(url_for('users.forget'))
        s = URLSafeTimedSerializer(app.secret_key)
        token = s.dumps(user.email, salt="RESET_PASSWORD")
        send_email(token,user.email)
        print(token)
        print("OK")
        return redirect(url_for('users.login'))
    return render_template('user/forget.html')


@user_blueprint.route('/new_password/<token>', methods=['GET','POST'])
def reset_password(token):
    s = URLSafeTimedSerializer(app.secret_key)
    email = s.loads(token, salt="RESET_PASSWORD", max_age=300)
    user= User(email=email).check_user()
    if not user:
        flash("invalid token")
        return redirect(url_for('users.root'))
    if request.method == "POST":
        if request.form['password'] != request.form['confirm']:
            flash("password not match")
            return redirect(url_for('users.reset_password'))
        user.set_password(request.form['password'])
        db.session.commit()
        return redirect(url_for('users.login'))
    
    return render_template('user/new_password.html')

@user_blueprint.route('/logout')
def log_out():
    logout_user()
    return render_template('user/login.html')