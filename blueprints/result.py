from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import ResultModel, SSModel
from forms import EditSSForm
import datetime as dt

blp = Blueprint("result", __name__)


# EDIT RESULTS ROUTE
@blp.route('/edit_result/<int:result_id>/ss<int:ss_id>', methods=["POST", "GET"])
def edit_result(result_id, ss_id):
    current_ss = db.get_or_404(SSModel, ss_id)
    print(f'current ss id is {current_ss.id}')
    form = EditSSForm()
    form.ss_label.label = f'SS {ss_id}'

    if request.method == "POST":
        form.validate_on_submit()
        microseconds = form.ss_1_t.data * pow(10, 5)
        # exec(
        #     f'current_result.ss_{ss_id} = dt.time(minute=form.ss_1_m.data, second=form.ss_1_s.data, microsecond=microseconds)')
        current_ss.time = dt.time(minute=form.ss_1_m.data, second=form.ss_1_s.data, microsecond=microseconds)
        db.session.commit()
        return redirect(url_for('event.event', event_id=current_ss.result.event_id))

    return render_template('edit_result.html', ss=current_ss, form=form)


# ADD RESULTS ROUTE
# @app.route('/add_results/<int:event_id>')
# def add_results(event_id):
#     current_event = db.get_or_404(Event, event_id)
#     return render_template('add_results.html', event=current_event)