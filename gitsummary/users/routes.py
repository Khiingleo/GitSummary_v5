from flask import Blueprint
from flask import request, render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from gitsummary import db, bcrypt
from gitsummary.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                              RequestResetForm, ResetPasswordForm)
from gitsummary.models import User
from gitsummary.users.utils import save_picture, send_reset_email




users = Blueprint('users', __name__)


@users.route("/register", strict_slashes=False, methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! you can now log in!", 'success')
        return redirect(url_for('users.login'))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", strict_slashes=False, methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.homepage'))
        else:
            flash("Login unsuccessful, please check email and password", 'danger')
    return render_template("login.html", title="login", form=form)


@users.route("/logout", strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))


@users.route("/account", strict_slashes=False, methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account Has Been Updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/reset_password', strict_slashes=False, methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("a token a has been sent to your email", 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="reset password", form=form)


@users.route('/reset_password/<token>', strict_slashes=False, methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    user = User.verify_reset_token(token)
    if not user:
        flash("Invalid Token or Token Has Expired", 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash(f"Your Password has been updated, You can now Log in!", 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset Password", form=form)