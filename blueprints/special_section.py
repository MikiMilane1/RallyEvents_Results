from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import ResultModel
from forms import EditSSForm

blp = Blueprint("special_section", __name__)

# SPECIAL SECTION ROUTE
@blp.route('/all_events')
def all_events():
    all_events_list = [item for item in EventModel.query.all()]
    return render_template('all_events.html', all_events=all_events_list)