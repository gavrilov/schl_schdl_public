from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Optional, ValidationError


def selection_validator(form, field):
    if field.data == 0:
        raise ValidationError("You have not selected school or grade")


class StudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired("Please enter First Name of Student")])
    last_name = StringField('Last Name', validators=[DataRequired("Please enter your Last Name of Student")])
    gender = SelectField('Gender', choices=[('1', 'Boy'), ('2', 'Girl')],
                         validators=[Optional("Please select Gender of Student")])
    dob = DateField('Date of Birth', validators=[InputRequired("Please enter Day of Birth")])
    default_school_id = SelectField('School', coerce=int, validators=[selection_validator])
    # current = BooleanField('Current Teacher')
    submit = SubmitField('Submit')
