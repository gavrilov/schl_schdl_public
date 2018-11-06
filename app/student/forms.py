from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Optional


class StudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired("Please enter First Name of Student")])
    last_name = StringField('Last Name', validators=[DataRequired("Please enter your Last Name of Student")])
    gender = SelectField('Gender', choices=[('1', 'Boy'), ('2', 'Girl')],
                         validators=[Optional("Please select Gender of Student")])
    dob = DateField('Date of Birth', validators=[InputRequired("Please enter Day of Birth")])
    # current = BooleanField('Current Teacher')
    submit = SubmitField('Submit')