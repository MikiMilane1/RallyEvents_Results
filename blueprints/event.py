from flask import Blueprint, render_template, request, redirect, url_for
from db import db
import os
from models import EventModel, EventEntryModel, DriverModel, SSModel, TeamModel
from forms import NewEventForm, NewEventEntryForm
import datetime as dt
import logging
APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, "templates", "event")

blp = Blueprint("event", __name__, template_folder=TEMPLATE_PATH)


# ALL EVENTS ROUTE
@blp.route('/all_events')
def all_events():
    all_events_list = [item for item in EventModel.query.all()]
    return render_template('all_events.html', all_events=all_events_list)


@blp.route('/event/<int:event_id>', methods=["POST", "GET"])
def event(event_id):
    current_event = db.get_or_404(EventModel, event_id)

    # GET EVENT ENTRY LIST
    event_entries = db.session.execute(db.select(EventEntryModel).filter_by(event_id=event_id)).scalars()

    # REGISTER DRIVER FORM
    new_entry_form = NewEventEntryForm()
    new_entry_form.team.choices = [item.name for item in TeamModel.query.all()]
    new_entry_form.submit.label.text = f'Register driver for {current_event.name}'

    # GET REGISTERED DRIVERS
    registered_drivers = current_event.drivers

    # GET UNREGISTERED DRIVERS
    unregistered_drivers = [item for item in db.session.query(DriverModel) if item not in registered_drivers]
    new_entry_form.driver.choices = [item.last_name + ', ' + item.first_name for item in unregistered_drivers]

    # SORT EVENT ENTRIES BY FINISH TIME
    event_entries_list = [item for item in current_event.event_entries]
    event_entries_list_sorted = sorted(event_entries_list, key=lambda x: x.finish_time, reverse=False)
    event_entries_list_sorted2 = sorted(event_entries_list, key=lambda x: x.finish_time, reverse=False)

    # SORT EVENT ENTRIES BY SPECIAL SECTIONS
    ss_dict = {'final': event_entries_list_sorted}
    for n in range(1, current_event.ss_total + 1):
        ss_sorted = SSModel.query.join(EventEntryModel).join(EventModel).filter(
            EventModel.id == current_event.id,
            SSModel.ss_num == n
        ).order_by(SSModel.time.asc()).all()
        logging.warning(msg=ss_sorted)
        ss_dict[f"ss_{n}"] = [item.event_entry for item in ss_sorted]

        afters_sorted = sorted(event_entries_list, key=lambda x: x.afters[n - 1], reverse=False)

        ss_dict[f"ss_{n}_after"] = afters_sorted

    logging.warning(msg=f"ssdict is {ss_dict}")

    if request.method == "POST" and new_entry_form.validate_on_submit():

        # REGISTERING DRIVER
        selected_driver_firstname = new_entry_form.driver.data.split(', ')[1]
        selected_driver_lastname = new_entry_form.driver.data.split(', ')[0]

        selected_driver = db.session.execute(db.select(DriverModel).filter_by(first_name=selected_driver_firstname,
                                                                              last_name=selected_driver_lastname)).scalar()
        current_event.drivers.append(selected_driver)
        db.session.commit()

        # CREATE EVENT_ENTRY
        new_event_entry = EventEntryModel(
            start_number=new_entry_form.start_number.data,
            car=new_entry_form.car.data,
            event_id=current_event.id,
            driver_id=selected_driver.id,
            team_id=TeamModel.query.filter(TeamModel.name == new_entry_form.team.data).first().id

        )
        db.session.add(new_event_entry)
        db.session.commit()

        # CREATE SPECIAL SECTIONS
        for n in range(1, new_event_entry.event.ss_total + 1):
            new_ss = SSModel(ss_num=n,
                             event_entry_id=new_event_entry.id,
                             time=dt.time(hour=0,
                                          minute=0,
                                          second=0,
                                          microsecond=0))
            db.session.add(new_ss)
            db.session.commit()

        return redirect(url_for('event.event', event_id=current_event.id))

    return render_template('event.html',
                           event=current_event,
                           register_driver_form=new_entry_form,
                           event_entry=event_entries,
                           ss_dict=ss_dict
                           )



