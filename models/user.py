from db import db
from flask_login import UserMixin


class UserModel(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
