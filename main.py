from __future__ import annotations
from dotenv import load_dotenv
import os
from db import db
from forms import LoginForm

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5

from blueprints.result import blp as ResultBP
from blueprints.driver import blp as DriverBP
from blueprints.event import blp as EventBP
from blueprints.search import blp as SearchBP
from blueprints.home import blp as HomeBP
from blueprints.edit_ss import blp as EditSSBP
from blueprints.add_and_edit_event import blp as AddEditEventBP

app = Flask(__name__)
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

app.register_blueprint(EventBP)
app.register_blueprint(DriverBP)
app.register_blueprint(ResultBP)
app.register_blueprint(SearchBP)
app.register_blueprint(HomeBP)
app.register_blueprint(EditSSBP)
app.register_blueprint(AddEditEventBP)


@app.route('/testing')
def testing():
    # return 'testing'
    form = LoginForm()
    return render_template('testing.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
