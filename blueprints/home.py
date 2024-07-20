from flask import Blueprint, render_template
import os
import datetime
from models import EventModel
import logging

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, "templates")

blp = Blueprint("home", __name__, template_folder=TEMPLATE_PATH)


@blp.route("/")
def index():
    live_events = [event for event in EventModel.query.all() if event.status == 'live']
    upcoming_events = [event for event in EventModel.query.all() if event.status == 'upcoming']
    return render_template('home/home.html', live_events=live_events, upcoming_events=upcoming_events)


@blp.route("/test")
def test():
    return render_template("testing.html")
