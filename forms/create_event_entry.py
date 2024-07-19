from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, DateField, FloatField, SelectField, IntegerField, FormField, HiddenField,
                     PasswordField, Label)
from wtforms.validators import DataRequired, URL


class NewEventEntryForm(FlaskForm):
    driver = SelectField(label='Register new driver', choices=[])
    start_number = IntegerField(label='Start number:')
    car = StringField(label='Car model:')
    team = SelectField(label='Team:', choices=[])
    submit = SubmitField(label='label')