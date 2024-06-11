from country_list import countries_for_language
from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from models import EventModel, ResultModel, DriverModel
from forms import NewEventForm, RegisterDriverForm

import logging

blp = Blueprint("event", __name__)


# ALL EVENTS ROUTE
@blp.route('/all_events')
def all_events():
    all_events_list = [item for item in EventModel.query.all()]
    print(all_events_list)
    return render_template('all_events.html', all_events=all_events_list)


@blp.route('/event/<int:event_id>', methods=["POST", "GET"])
def event(event_id):
    current_event = db.get_or_404(EventModel, event_id)

    # GET RESULTS LIST
    results = db.session.execute(db.select(R).filter_by(event_id=event_id)).scalars()
    logging.warning(f'results is {results}')

    # REGISTER DRIVER FORM
    register_driver_form = RegisterDriverForm()
    register_driver_form.submit.label.text = f'Register driver for {current_event.name}'

    # GET REGISTERED DRIVERS
    registered_drivers = current_event.drivers

    # GET UNREGISTERED DRIVERS
    unregistered_drivers = [item for item in db.session.query(DriverModel) if item not in registered_drivers]
    register_driver_form.driver.choices = [item.last_name + ', ' + item.first_name for item in unregistered_drivers]

    # TODO organize results
    # TODO lookup arrays
    # SORT RESULTS
    # try:
    #     results_list = [item for item in current_event.results]
    #     logging.warning(f'showing the results list {results_list}')
    #     results_list_organized = [{'ss_1': item.ss_1,
    #                                'ss_2': item.ss_2,
    #                                'after ss_2': add_time(item.ss_1, item.ss_2),
    #                                'ss_3': item.ss_3,
    #                                'after ss_3': add_time(item.ss_1, item.ss_2, item.ss_3),
    #                                'ss_4': item.ss_4,
    #                                'after ss_4': add_time(item.ss_1, item.ss_2, item.ss_3, item.ss_4),
    #                                'ss_5': item.ss_5,
    #                                'final': add_time(item.ss_1, item.ss_2, item.ss_3, item.ss_4, item.ss_5)} for item in results_list]
    #     print(results_list_organized)
    # except AttributeError:
    #     results_list_organized = []
    # CREATE DICT ENTRY FROM
    results_list_organized = []
    if request.method == "POST" and register_driver_form.validate_on_submit():
        logging.warning('submitting driver form')

        # REGISTERING DRIVER
        selected_driver_firstname = register_driver_form.driver.data.split(', ')[1]
        selected_driver_lastname = register_driver_form.driver.data.split(', ')[0]

        selected_driver = db.session.execute(db.select(Driver).filter_by(first_name=selected_driver_firstname,
                                                                         last_name=selected_driver_lastname)).scalar()
        current_event.drivers.append(selected_driver)
        db.session.commit()

        # CREATE RESULT ENTRY
        new_result = ResultModel(
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
                           register_driver_form=register_driver_form, ss_num=current_event,
                           test_dict=results_list_organized
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
        print(f'the year youre looking for is {form.date_from.data.year}')

        print(f'trying out {form.data}')

        # ADD EVENT TO DB
        new_event = EventModel(
            name=form.name.data,
            series=form.series.data,
            series_instance=form.series_instance.data,
            date_from=form.date_from.data,
            date_to=form.date_to.data,
            location=form.location.data,
            country=form.country.data,
            year=form.date_from.data.year,
            surface=form.surface.data,
            distance=form.distance.data,
            ss_num=form.ss_num.data
        )
        db.session.add(new_event)
        db.session.commit()

        # REQUESTING ADDED EVENT FOR REDIRECT
        requested_event = db.session.execute(db.select(Event).filter_by(name=form.name.data)).scalar()

        return redirect(url_for('event', event_id=requested_event.id))
    return render_template('new_event.html', form=form)
