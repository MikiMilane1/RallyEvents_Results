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
    start_number = IntegerField(label='Start number')
    submit = SubmitField(label='label')


# SEARCH FORM
class SearchForm(FlaskForm):
    searched = StringField()


# EDIT RESULT FORM
class EditSSForm(FlaskForm):
    # SS1
    ss_label = HiddenField(label='SS 1')
    ss_1_m = IntegerField(label='', render_kw={"placeholder": "minutes"})
    ss_1_s = IntegerField(label='', render_kw={"placeholder": "seconds"})
    ss_1_t = IntegerField(label='', render_kw={"placeholder": "tenths"})
    submit = SubmitField(label="Apply edits")


class TelephoneForm(FlaskForm):
    country_code = IntegerField('Country Code')
    area_code = IntegerField('Area Code/Exchange')
    number = StringField('Number')


class ContactForm(FlaskForm):
    first_name = StringField()
    last_name = StringField()
    mobile_phone = FormField(TelephoneForm)
    office_phone = FormField(TelephoneForm)


class login_form(FlaskForm):
    some_hiden_field = HiddenField()
    username = StringField('User Name :', validators=[DataRequired()])
    password = PasswordField('Password :', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')
