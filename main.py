from __future__ import annotations
from dotenv import load_dotenv
import os
from db import db
from forms import LoginForm

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5

from functions import register_bps

from blueprints import AddEditEventBP, EventEntryBP, EventBP, SearchBP, HomeBP, EditSSBP, TeamBP, UserBP, DriverBP

app = Flask(__name__)
app.config["DEBUG"] = True
Bootstrap5(app)


def configure():
    load_dotenv()


configure()

# CSRF SECRET KEY
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"
db.init_app(app)

with app.app_context():
    db.create_all()

register_bps(app, EventBP, DriverBP, EventEntryBP, SearchBP, HomeBP, EditSSBP, AddEditEventBP, TeamBP, UserBP)


@app.route('/testing')
def testing():
    # return 'testing'
    form = LoginForm()
    return render_template('testing.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
