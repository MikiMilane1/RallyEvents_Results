from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, DateField, FloatField, SelectField, IntegerField, FormField, HiddenField,
                     PasswordField, Label)
from wtforms.validators import DataRequired, URL


class EditSSForm(FlaskForm):
    # SS1
    ss_label = HiddenField(label='SS 1')
    ss_1_m = IntegerField(label='', render_kw={"placeholder": "minutes"})
    ss_1_s = IntegerField(label='', render_kw={"placeholder": "seconds"})
    ss_1_t = IntegerField(label='', render_kw={"placeholder": "tenths"})
    submit = SubmitField(label="Apply edits")
