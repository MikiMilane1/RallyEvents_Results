from flask import Blueprint, render_template, redirect, url_for, request
from db import db
import os
from models import EventEntryModel, SSModel
from forms import EditSSForm
import datetime as dt

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, "templates")

blp = Blueprint("edit_ss", __name__, template_folder=TEMPLATE_PATH)


# SPECIAL SECTION ROUTE
@blp.route('/edit_ss/<int:ss_id>', methods=["POST", "GET"])
def edit_ss(ss_id):
    current_ss = db.get_or_404(SSModel, ss_id)
    form = EditSSForm()
    form.ss_label.label = f'SS {ss_id}'

    if request.method == "POST":
        form.validate_on_submit()
        microseconds = form.ss_1_t.data * pow(10, 5)
        if microseconds == 0:
            microseconds = 1
        current_ss.time = dt.time(minute=form.ss_1_m.data, second=form.ss_1_s.data, microsecond=microseconds)
        db.session.commit()
        return redirect(url_for('event.event', event_id=current_ss.result.event_id))

    return render_template("edit_ss.html", ss=current_ss, form=form)
