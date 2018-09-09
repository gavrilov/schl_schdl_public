from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Optional


class StudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired("Please enter First Name of Student")])
    last_name = StringField('Last Name', validators=[DataRequired("Please enter your Last Name of Student")])
    gender = BooleanField('Gender',
                          validators=[Optional("Please select Gender of Student")])  # True = boy, False = girl
    dob = DateField('Date of Birth', validators=[InputRequired("Please enter Day of Birth")])
    # current = BooleanField('Current Teacher')
    submit = SubmitField('Submit')