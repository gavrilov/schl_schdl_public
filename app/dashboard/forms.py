from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional


class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired("Please enter your First Name")])
    last_name = StringField('Last Name', validators=[DataRequired("Please enter your Last Name")])
    email = StringField('Email', validators=[Optional()])
    submit = SubmitField('Submit')


