from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FloatField, SelectField, IntegerField
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
    distance = FloatField(label="Distance:", validators=[DataRequired()])

    submit = SubmitField(label='Create new event entry')


# ADD NEW DRIVER TO DB
class NewDriverForm(FlaskForm):
    firstname = StringField(label="First name:", validators=[DataRequired()])
    lastname = StringField(label="Last name:", validators=[DataRequired()])

    country = SelectField(label='Country:', choices=country_names_list, validators=[DataRequired()])
    birth_date = DateField(label='Date of birth:', validators=[DataRequired()])
    submit = SubmitField(label='Create new driver entry')


# REGISTER DRIVER TO EVENT
class RegisterDriverForm(FlaskForm):
    driver = SelectField(label='Register new driver', choices=[])
    submit = SubmitField(label='label')


# SEARCH FORM
class SearchForm(FlaskForm):
    searched = StringField(render_kw={'style': 'width: 30ch'})
