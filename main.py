from __future__ import annotations
from typing import List
from dotenv import load_dotenv
import os
import logging
import datetime as dt

import sqlalchemy.exc
from flask import Flask, render_template, request, redirect, url_for
from forms import NewDriverForm, NewEventForm, RegisterDriverForm, SearchForm, EditSSForm, TelephoneForm, login_form
from wtforms import Label
from flask_bootstrap import Bootstrap5

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Float, Date, Table, Column, select, Time

from country_list import countries_for_language

app = Flask(__name__)
Bootstrap5(app)


def configure():
    load_dotenv()


configure()

# CSRF SECRET KEY
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# TODO add route protection


# INNIT SQL AND CREATE TABLES---------------------------------

# INIT SQL DATABASE
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///event_driver_result.sqlite"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLES

# ASSOCIATION TABLE
association_table = Table('association_table',
                          Base.metadata,
                          Column("event_id", ForeignKey("events.id"), primary_key=True),
                          Column("driver_id", ForeignKey("drivers.id"), primary_key=True),
                          )


# EVENT TABLE
class Event(db.Model):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(250), nullable=False)
    series: Mapped[str] = mapped_column(String(250), nullable=True)
    series_instance: Mapped[int] = mapped_column(Integer, nullable=True)
    # TODO create series DB and convert it to selectfield in the form
    year: Mapped[int] = mapped_column(Integer)
    date_from: Mapped[str] = mapped_column(Date, nullable=False)
    date_to: Mapped[str] = mapped_column(Date, nullable=False)
    country: Mapped[str] = mapped_column(String(3), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    surface: Mapped[str] = mapped_column(String(250), nullable=False)
    distance: Mapped[float] = mapped_column(Float, nullable=True)

    # ASSOCIATE EVENT WITH DRIVERS
    drivers: Mapped[List[Driver]] = relationship(secondary=association_table, back_populates="events")
    # ASSOCIATE EVENT WITH RESULTS
    results = relationship("Result", back_populates="event")


# DRIVER TABLE
class Driver(db.Model):
    __tablename__ = "drivers"
    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    birth_date: Mapped[str] = mapped_column(Date, nullable=False)
    country: Mapped[str] = mapped_column(String(40), nullable=False)

    # ASSOCIATE WITH EVENTS(MtM) and RESULTS(OtM)
    events: Mapped[List[Event]] = relationship(secondary=association_table, back_populates="drivers")
    results = relationship("Result", back_populates="driver")


# RESULT TABLE
class Result(db.Model):
    __tablename__ = 'results'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_number: Mapped[int] = mapped_column(Integer, nullable=False)
    ss_1 = mapped_column(Time, nullable=True)
    ss_2 = mapped_column(Time, nullable=True)
    ss_3 = mapped_column(Time, nullable=True)
    ss_4 = mapped_column(Time, nullable=True)
    ss_5 = mapped_column(Time, nullable=True)



    # ASSOCIATE WITH EVENT(OtM) AND DRIVER(OtM)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id'))
    event = relationship("Event", back_populates="results")
    driver_id: Mapped[int] = mapped_column(ForeignKey('drivers.id'))
    driver = relationship("Driver", back_populates="results")


with app.app_context():
    db.create_all()


# ROUTES------------------------------------

# HOME ROUTE
@app.route('/')
def index():
    # ADD EVENTS FROM DB TO LIST
    showcase_events = [item for item in db.session.query(Event).limit(3)]

    return render_template('index.html', showcase_events=showcase_events)


# ADD EVENT ROUTE
@app.route('/add_event', methods=["POST", "GET"])
def create_new_event():
    country_names = {name: code for code, name in countries_for_language('en')}
    country_names_list = list(country_names.keys())

    form = NewEventForm()
    form.country.choices = country_names_list

    if request.method == "POST":
        form.validate_on_submit()
        print(f'the year youre looking for is {form.date_from.data.year}')

        # ADD EVENT TO DB
        new_event = Event(
            name=form.name.data,
            series=form.series.data,
            series_instance=form.series_instance.data,
            date_from=form.date_from.data,
            date_to=form.date_to.data,
            location=form.location.data,
            country=form.country.data,
            year=form.date_from.data.year,
            surface=form.surface.data,
            distance=form.distance.data)
        db.session.add(new_event)
        db.session.commit()

        # REQUESTING ADDED EVENT FOR REDIRECT
        requested_event = db.session.execute(db.select(Event).filter_by(name=form.name.data)).scalar()

        return redirect(url_for('event', event_id=requested_event.id))
    return render_template('new_event.html', form=form)


# SINGLE EVENT ROUTE
@app.route('/event/<int:event_id>', methods=["POST", "GET"])
def event(event_id):
    current_event = db.get_or_404(Event, event_id)

    # GET RESULTS LIST
    results = db.session.execute(db.select(Result).filter_by(event_id=event_id)).scalars()
    logging.warning(f'results is {results}')

    # REGISTER DRIVER FORM
    register_driver_form = RegisterDriverForm()
    register_driver_form.submit.label.text = f'Register driver for {current_event.name}'


    # GET REGISTERED DRIVERS
    registered_drivers = current_event.drivers

    # GET UNREGISTERED DRIVERS
    unregistered_drivers = [item for item in db.session.query(Driver) if item not in registered_drivers]
    register_driver_form.driver.choices = [item.last_name + ', ' + item.first_name for item in unregistered_drivers]

    if request.method == "POST" and register_driver_form.validate_on_submit():
        logging.warning('submitting driver form')

        # REGISTERING DRIVER
        selected_driver_firstname = register_driver_form.driver.data.split(', ')[1]
        selected_driver_lastname = register_driver_form.driver.data.split(', ')[0]

        selected_driver = db.session.execute(db.select(Driver).filter_by(first_name=selected_driver_firstname,
                                                                         last_name=selected_driver_lastname)).scalar()
        current_event.drivers.append(selected_driver)
        db.session.commit()

        # CREATING RESULT ENTRY
        new_result = Result(
            start_number=register_driver_form.start_number.data,
            event_id=current_event.id,
            driver_id=selected_driver.id,
        )
        db.session.add(new_result)
        db.session.commit()

        logging.warning(f'the type is {type(current_event.results)}')

        return redirect(url_for('event', event_id=current_event.id))

    return render_template('event.html',
                           event=current_event,
                           register_driver_form=register_driver_form,
                           )


# SINGLE DRIVER ROUTE
@app.route('/driver/<int:driver_id>')
def driver(driver_id):
    requested_driver = db.get_or_404(Driver, driver_id)
    print(requested_driver.first_name + requested_driver.last_name)

    return render_template('driver.html', driver=requested_driver)


# ADD NEW DRIVER ROUTE
@app.route('/add_driver', methods=["POST", "GET"])
def add_new_driver():
    form = NewDriverForm()

    if request.method == "POST":
        print('driver data submitted')
        form.validate_on_submit()

        # ADD DRIVER TO DB
        new_driver = Driver(
            first_name=form.firstname.data,
            last_name=form.lastname.data,
            birth_date=form.birth_date.data,
            country=form.country.data)
        db.session.add(new_driver)
        db.session.commit()

        # REQUESTING ADDED DRIVER FOR REDIRECT
        requested_driver = db.session.execute(
            db.select(Driver).filter_by(first_name=form.firstname.data, last_name=form.lastname.data)).scalar()
        print(
            f'the driver id for {requested_driver.first_name} + {requested_driver.last_name} is {requested_driver.id}')

        return redirect(url_for('driver', driver_id=requested_driver.id))
    return render_template('new_driver.html', form=form)


# ALL DRIVERS ROUTE
@app.route('/all_drivers')
def all_drivers():
    all_drivers = []
    for driver in db.session.query(Driver):
        all_drivers.append(driver.__dict__)
    return render_template('all_drivers.html', all_drivers=all_drivers)


# ALL EVENTS ROUTE
@app.route('/all_events')
def all_events():
    all_events = []
    for row in db.session.query(Event):
        all_events.append(row.__dict__)
    print(all_events)
    # TODO divide events into current, future and past events
    return render_template('all_events.html', all_events=all_events)


# REMOVE DRIVER FROM EVENT
@app.route('/remove_driver from event/<int:event_id>/<int:driver_id>')
def remove_driver_from_event(event_id, driver_id):
    current_event = db.get_or_404(Event, event_id)
    current_driver = db.get_or_404(Driver, driver_id)
    current_event.drivers.remove(current_driver)
    db.session.commit()
    return redirect(url_for('event', event_id=event_id))


# SEARCH ROUTE
@app.route('/search', methods=["POST"])
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


# ADD RESULTS ROUTE
# @app.route('/add_results/<int:event_id>')
# def add_results(event_id):
#     current_event = db.get_or_404(Event, event_id)
#     return render_template('add_results.html', event=current_event)

# EDIT RESULTS ROUTE
@app.route('/edit_result/<int:result_id>/ss<int:ss_id>', methods=["POST", "GET"])
def edit_result(result_id, ss_id):
    current_result = db.get_or_404(Result, result_id)
    form = EditSSForm()
    form.ss_label.label = f'SS {ss_id}'

    if request.method == "POST":
        form.validate_on_submit()
        microseconds = form.ss_1_t.data * pow(10, 5)
        exec(f'current_result.ss_{ss_id} = dt.time(minute=form.ss_1_m.data, second=form.ss_1_s.data, microsecond=microseconds)')

        db.session.commit()
        return redirect(url_for('event', event_id=current_result.event_id))

    return render_template('edit_result.html', result=current_result, form=form)


# TODO login button functionality

# TODO edit event and edit driver routes

@app.route('/testing')
def testing():
    form = login_form()
    return render_template('testing.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
