from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, DateField, FloatField, SelectField, IntegerField, FormField, HiddenField,
                     PasswordField, Label)
from wtforms.validators import DataRequired, URL


class RegisterDriverForm(FlaskForm):
    driver = SelectField(label='Register new driver', choices=[])
    start_number = IntegerField(label='Start number')
    submit = SubmitField(label='label')