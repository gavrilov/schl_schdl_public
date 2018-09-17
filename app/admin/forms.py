from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional


class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired("Please enter your First Name")])
    last_name = StringField('Last Name', validators=[DataRequired("Please enter your Last Name")])
    email = StringField('Email', validators=[Optional()])
    submit = SubmitField('Submit')


class SchoolForm(FlaskForm):
    name = StringField('School Name', validators=[DataRequired()])
    director_name = StringField('Director Name', validators=[Optional()])
    note = StringField('Note', validators=[Optional()])
    current = BooleanField('Current School')
    # password = StringField('Password', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired()])
    # easypost_api_key = StringField('EasyPost API Key', validators=[DataRequired()])
    submit = SubmitField('Submit')
