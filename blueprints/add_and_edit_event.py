from country_list import countries_for_language
from flask import Blueprint, render_template, request, redirect, url_for
from db import db
import os
from models import EventModel, EventEntryModel, DriverModel, SSModel
from forms import NewEventForm, RegisterDriverForm
import datetime as dt
import logging

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, "templates")

blp = Blueprint("add_and_edit_event", __name__, template_folder=TEMPLATE_PATH)


# ADD EVENT ROUTE
@blp.route('/add_event', methods=["POST", "GET"])
def create_new_event():
    country_names = {name: code for code, name in countries_for_language('en')}
    country_names_list = list(country_names.keys())

    form = NewEventForm()
    form.country.choices = country_names_list

    if request.method == "POST":
        form.validate_on_submit()

        # ADD EVENT TO DB
        event_data = {k: v for k, v in form.data.items() if k != "submit" and k != "csrf_token"}
        new_event = EventModel(**event_data)
        db.session.add(new_event)
        db.session.commit()

        # REQUESTING ADDED EVENT FOR REDIRECT
        requested_event = new_event

        return redirect(url_for('event.event', event_id=requested_event.id))
    return render_template('new_event.html', form=form)


# EDIT EVENT ROUTE
@blp.route('/edit_event/<int:event_id>', methods=["POST", "GET"])
def edit_event(event_id):
    event = db.get_or_404(EventModel, event_id)
    form = NewEventForm()
    if request.method == 'GET':
        return 'Well hello there!'
    return render_template('edit_event.html', event=event, form=form)
