from flask import request, Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from route.forms import User, RegistrationForm, LoginForm
from config import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

fetch = Blueprint('fetch', __name__)


@fetch.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            message = 'Вы уже зарегистрированы'
            return render_template('register.html', form=form, message=message)
        hash = generate_password_hash(password)
        NewUser = User(
            email=email,
            name=name,
            password=hash
        )
        db.session.add(NewUser)
        db.session.commit()
        return redirect(url_for('fetch.login_post'))
    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))


@fetch.route('/login', methods=['GET', 'POST'])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            message = 'Неверный пароль'
            return render_template('login.html', form=form, message=message)
        login_user(user, remember=remember)
        return redirect(url_for('fetch.profile'))
    return render_template('login.html', form=form)


@fetch.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@fetch.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('fetch.login_post'))