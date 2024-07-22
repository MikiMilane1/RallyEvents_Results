from flask import Blueprint, render_template, request, redirect, url_for
from db import db
import os
from forms import NewUserForm
from models import TeamModel, UserModel
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, "templates", "user")

blp = Blueprint("user", __name__, template_folder=TEMPLATE_PATH)


@blp.route("/register", methods=["POST", "GET"])
def register():

    form = NewUserForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = UserModel(
            username=form.username.data,
            password_hash=pbkdf2_sha256.hash(form.password.data)
        )
        db.session.add(UserModel)
        db.session.commit()
        return render_template('user_info.html', user=user)

    return render_template('register.html')
