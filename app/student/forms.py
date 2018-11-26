from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Optional, ValidationError
from flask import flash


def selection_validator(form, field):
    if field.data == 0 or field.data == '0':
        flash('You have not selected {} '.format(field.label.text), 'danger')
        raise ValidationError("You have not selected school or grade")


class StudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired("Please enter First Name of Student")])
    last_name = StringField('Last Name', validators=[DataRequired("Please enter your Last Name of Student")])
    gender = SelectField('Gender', choices=[('0', '---'), ('1', 'Boy'), ('2', 'Girl')],
                         validators=[selection_validator])
    dob = DateField('Date of Birth', validators=[InputRequired("Please enter Day of Birth")])
    default_school_id = SelectField('School', coerce=int, validators=[selection_validator])
    grade = SelectField('Grade', choices=[(0, '---'), (-3, 'Preschool'), (-2, 'Pre-Kindergarten'), (-1, 'Kindergarten'),
                                          (1, '1st'), (2, '2nd'), (3, '3rd'), (4, '4th'), (5, '5th')], coerce=int,
                        validators=[selection_validator])
    submit = SubmitField('Submit')
