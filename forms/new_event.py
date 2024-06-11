from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, DateField, FloatField, SelectField, IntegerField, FormField, HiddenField,
                     PasswordField, Label)
from wtforms.validators import DataRequired, URL
from country_list import countries_for_language

# GET LIST OF COUNTRIES
country_names = {name: code for code, name in countries_for_language('en')}
country_names_list = list(country_names.keys())


# ADD NEW EVENT TO DB
class NewEventForm(FlaskForm):
    # GET LIST OF COUNTRIES
    country_names = {name: code for code, name in countries_for_language('en')}
    country_names_list = list(country_names.keys())

    name = StringField(label="Event name:", validators=[DataRequired()])
    series = StringField(label="Series:")
    series_instance = IntegerField(label="Series instance:")
    date_from = DateField(label='Date from:', validators=[DataRequired()])
    date_to = DateField(label='Date to:', validators=[DataRequired()])
    country = SelectField(label="Country:", validators=[DataRequired()])
    location = StringField(label="Location:", validators=[DataRequired()])
    surface = SelectField(label="Surface:", choices=['gravel', 'asphalt'])
    ss_num = IntegerField(label="Number of special sections:")
    distance = FloatField(label="Distance:", validators=[DataRequired()])

    submit = SubmitField(label='Create new event entry')