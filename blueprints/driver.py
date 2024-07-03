from flask import Blueprint, render_template, request, redirect, url_for
from db import db
import os
from forms import NewDriverForm
from models import DriverModel, EventModel
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import MultiDict

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, "templates", "driver")

blp = Blueprint("driver", __name__, template_folder=TEMPLATE_PATH)


@blp.route('/all_drivers')
def all_drivers():
    all_drivers_list = [item.__dict__ for item in DriverModel.query.all()]
    return render_template('all_drivers.html', all_drivers=all_drivers_list)


@blp.route('/add_driver', methods=["POST", "GET"])
def add_new_driver():
    form = NewDriverForm(formdata=MultiDict({'firstname': 'Foo'}))

    if request.method == "POST":
        form.validate_on_submit()

        # ADD DRIVER TO DB
        new_driver = DriverModel(
            first_name=form.firstname.data,
            last_name=form.lastname.data,
            birth_date=form.birth_date.data,
            country=form.country.data)
        try:
            db.session.add(new_driver)
            db.session.commit()
        except IntegrityError:
            return 'Driver with that name and birth date already exists in the database.'

        return redirect(url_for('driver.driver', driver_id=new_driver.id))
    return render_template('new_driver.html', form=form)


# SINGLE DRIVER ROUTE
@blp.route('/driver/<int:driver_id>')
def driver(driver_id):
    requested_driver = db.get_or_404(DriverModel, driver_id)
    print(requested_driver.first_name + requested_driver.last_name)

    return render_template('driver.html', driver=requested_driver)


# EDIT DRIVER ROUTE
@blp.route("/edit_driver/<int:driver_id>", methods=["POST", "GET"])
def edit_driver(driver_id):
    driver = db.get_or_404(DriverModel, driver_id)
    form = NewDriverForm()

    if request.method == 'GET':
        form.firstname.data = driver.first_name
        form.lastname.data = driver.last_name
        form.country.data = driver.country
        form.birth_date.data = driver.birth_date
        form.submit.label.text = 'Submit edit'

    if request.method == "POST":
        form.validate_on_submit()
        print(form.data)

        driver.first_name = form.firstname.data
        driver.last_name = form.lastname.data
        driver.country = form.country.data
        driver.birth_date = form.birth_date.data
        db.session.add(driver)
        db.session.commit()
        return redirect(url_for('driver.driver', driver_id=driver_id))

    return render_template('edit_driver.html', form=form)


# REMOVE DRIVER FROM EVENT
@blp.route('/remove_driver_from_event/<int:event_id>/<int:driver_id>')
def remove_driver_from_event(event_id, driver_id):
    current_event = db.get_or_404(EventModel, event_id)
    current_driver = db.get_or_404(DriverModel, driver_id)
    current_event.drivers.remove(current_driver)
    db.session.commit()
    return redirect(url_for('event', event_id=event_id))
