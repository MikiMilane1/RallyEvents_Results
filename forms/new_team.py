from country_list import countries_for_language
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, DateField, FloatField, SelectField, IntegerField, FormField, HiddenField,
                     PasswordField, Field)
from wtforms.validators import DataRequired, URL
from wtforms.widgets import html_params
from wtforms.fields import Field
from markupsafe import Markup

country_names = {name: code for code, name in countries_for_language('en')}
country_names_list = list(country_names.keys())


class BreakField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, **kwargs):
        return Markup('<div style="margin: 10px 0;"></div>')

class NewTeamForm(FlaskForm):
    name = StringField(label="Team name:", validators=[DataRequired()])
    country = SelectField(label='Country:', choices=country_names_list, validators=[DataRequired()])
    socials = BreakField()
    socials_ig = StringField(label="Instagram:")
    socials_twitter = StringField(label="Twitter:")
    submit = SubmitField(label='Create new team entry')
