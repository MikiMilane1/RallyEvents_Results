from flask import Blueprint, render_template, redirect, url_for
from db import db
from models import DriverModel

blp = Blueprint("search", __name__)


# SEARCH ROUTE
@blp.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    searched = form.searched.data

    # GET SEARCH RESULTS
    event_names = [item.name for item in db.session.query(Event)]
    driver_names = []
    for item in db.session.query(Driver):
        if searched in item.first_name or searched in item.last_name:
            driver_names.append(item)

    results_events = [item for item in event_names if searched in item]
    results_drivers = driver_names

    return render_template('search_results.html', results_drivers=results_drivers, results_events=results_events)
