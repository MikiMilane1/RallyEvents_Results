from country_list import countries_for_language
from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from models import EventModel, ResultModel, DriverModel, SSModel
from forms import NewEventForm, RegisterDriverForm
import datetime as dt
import logging

blp = Blueprint("event", __name__)


# ALL EVENTS ROUTE
@blp.route('/all_events')
def all_events():
    all_events_list = [item for item in EventModel.query.all()]
    return render_template('all_events.html', all_events=all_events_list)


@blp.route('/event/<int:event_id>', methods=["POST", "GET"])
def event(event_id):
    current_event = db.get_or_404(EventModel, event_id)

    # GET RESULTS LIST
    results = db.session.execute(db.select(ResultModel).filter_by(event_id=event_id)).scalars()

    # REGISTER DRIVER FORM
    register_driver_form = RegisterDriverForm()
    register_driver_form.submit.label.text = f'Register driver for {current_event.name}'

    # GET REGISTERED DRIVERS
    registered_drivers = current_event.drivers

    # GET UNREGISTERED DRIVERS
    unregistered_drivers = [item for item in db.session.query(DriverModel) if item not in registered_drivers]
    register_driver_form.driver.choices = [item.last_name + ', ' + item.first_name for item in unregistered_drivers]

    # SORT RESULTS BY FINISH TIME
    results_list = [item for item in current_event.results]
    print(f"unorganized list is {results_list}")

    results_list_sorted = sorted(results_list, key=lambda x: x.finish_time, reverse=True)
    print(f"sorted list is {results_list_sorted}")
    print('finish times are')
    for item in results_list_sorted:
        print(item.finish_time)

    if request.method == "POST" and register_driver_form.validate_on_submit():
        logging.warning('submitting driver form')

        # REGISTERING DRIVER
        selected_driver_firstname = register_driver_form.driver.data.split(', ')[1]
        selected_driver_lastname = register_driver_form.driver.data.split(', ')[0]

        selected_driver = db.session.execute(db.select(DriverModel).filter_by(first_name=selected_driver_firstname,
                                                                              last_name=selected_driver_lastname)).scalar()
        current_event.drivers.append(selected_driver)
        db.session.commit()

        # CREATE RESULT ENTRY
        new_result = ResultModel(
            start_number=register_driver_form.start_number.data,
            car=register_driver_form.car.data,
            event_id=current_event.id,
            driver_id=selected_driver.id,
        )
        db.session.add(new_result)
        db.session.commit()

        # CREATE SPECIAL SECTIONS
        for n in range(1, new_result.event.ss_num + 1):
            new_ss = SSModel(ss_num=n,
                             result_id=new_result.id,
                             time=dt.time(hour=0,
                                          minute=0,
                                          second=0,
                                          microsecond=0))
            db.session.add(new_ss)
            db.session.commit()

        return redirect(url_for('event.event', event_id=current_event.id))

    print(f'drivers for this events are {current_event.drivers}')
    return render_template('event.html',
                           event=current_event,
                           register_driver_form=register_driver_form, ss_num=current_event,
                           results=results_list_sorted
                           )


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
        print(form.data)
        event_data = {k: v for k, v in form.data.items() if k != "submit" and k != "csrf_token"}
        new_event = EventModel(**event_data)
        db.session.add(new_event)
        db.session.commit()

        # REQUESTING ADDED EVENT FOR REDIRECT
        requested_event = new_event

        return redirect(url_for('event.event', event_id=requested_event.id))
    return render_template('new_event.html', form=form)
