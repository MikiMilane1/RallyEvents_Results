from country_list import countries_for_language
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, DateField, FloatField, SelectField, IntegerField, FormField, HiddenField,
                     PasswordField, Label)
from wtforms.validators import DataRequired, URL

country_names = {name: code for code, name in countries_for_language('en')}
country_names_list = list(country_names.keys())

class NewDriverForm(FlaskForm):
    firstname = StringField(label="First name:", validators=[DataRequired()])
    lastname = StringField(label="Last name:", validators=[DataRequired()])

    country = SelectField(label='Country:', choices=country_names_list, validators=[DataRequired()])
    birth_date = DateField(label='Date of birth:', validators=[DataRequired()])
    submit = SubmitField(label='Create new driver entry')