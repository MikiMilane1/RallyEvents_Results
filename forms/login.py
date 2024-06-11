from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, DateField, FloatField, SelectField, IntegerField, FormField, HiddenField,
                     PasswordField, Label)
from wtforms.validators import DataRequired, URL


class LoginForm(FlaskForm):
    some_hiden_field = HiddenField()
    username = StringField('User Name :', validators=[DataRequired()])
    password = PasswordField('Password :', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')