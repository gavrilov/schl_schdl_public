from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired("Please enter your First Name")])
    last_name = StringField('Last Name', validators=[DataRequired("Please enter your Last Name")])
    email = StringField('Email', validators=[DataRequired("Please enter your Last Name")])
    submit = SubmitField('Submit')
