from flask import Blueprint, render_template, request, redirect, url_for
from db import db
import os
from forms import NewUserForm
from models import TeamModel, UserModel
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from extensions import login_manager

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, "templates", "user")

blp = Blueprint("user", __name__, template_folder=TEMPLATE_PATH)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(UserModel, user_id)


@blp.route("/register", methods=["POST", "GET"])
def register():
    form = NewUserForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = UserModel(
            username=form.username.data,
            password_hash=pbkdf2_sha256.hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        return render_template('dashboard.html', form=form, user=user)

    return render_template('register.html', form=form)


@blp.route("/login", methods=["POST", "GET"])
def login():
    form = NewUserForm()
    if request.method == "POST" and form.validate_on_submit():
        user = UserModel.query.filter(UserModel.username == form.username.data).first()
        if user:
            pass

    form.submit.label.text = 'Login'
    return render_template('login.html', form=form)


@blp.route("/logout", methods=["POST", "GET"])
def logout():
    return 'Successfully logged out.'


@blp.route("/dashboard/<int:user_id>")
def dashboard(user_id):
    user = db.get_or_404(UserModel, user_id)
    return render_template('dashboard.html', user=user)
