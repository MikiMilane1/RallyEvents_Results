from flask import Blueprint, render_template
import os
APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, "templates")

blp = Blueprint("home", __name__, template_folder=TEMPLATE_PATH)


@blp.route("/")
def index():
    # return "Home"
    return render_template('index1.html')
