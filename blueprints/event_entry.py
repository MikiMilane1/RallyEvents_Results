from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import EventEntryModel, SSModel
from forms import EditSSForm
import datetime as dt

blp = Blueprint("event_entry", __name__)


# EDIT EVENT_ENTRY ROUTE
@blp.route('/edit_event_entry/<int:event_entry_id>/ss<int:ss_id>', methods=["POST", "GET"])
def edit_event_entry(event_entry_id, ss_id):
    current_ss = db.get_or_404(SSModel, ss_id)
    form = EditSSForm()
    form.ss_label.label = f'SS {ss_id}'

    if request.method == "POST":
        form.validate_on_submit()
        microseconds = form.ss_1_t.data * pow(10, 5)
        current_ss.time = dt.time(minute=form.ss_1_m.data, second=form.ss_1_s.data, microsecond=microseconds)
        db.session.commit()
        return redirect(url_for('event.event', event_id=current_ss.event_entry.event_id))

    return render_template('edit_event_entry.html', ss=current_ss, form=form)


# ADD RESULTS ROUTE
# @app.route('/add_results/<int:event_id>')
# def add_results(event_id):
#     current_event = db.get_or_404(Event, event_id)
#     return render_template('add_results.html', event=current_event)