from country_list import countries_for_language
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, DateField, FloatField, SelectField, IntegerField, FormField, HiddenField,
                     PasswordField, Field)
from wtforms.validators import DataRequired, URL
from wtforms.widgets import html_params
from wtforms.fields import Field

country_names = {name: code for code, name in countries_for_language('en')}
country_names_list = list(country_names.keys())


class NewUserForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = StringField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Register')

class LoginForm(FlaskForm):
    username = StringField()