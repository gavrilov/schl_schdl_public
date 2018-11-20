from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField, BooleanField, TextAreaField, IntegerField, StringField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import Optional


class ClassForm(FlaskForm):
    school_id = SelectField('School', coerce=int, validators=[Optional()])
    teacher_id = SelectField('Teacher', coerce=int, validators=[Optional()])
    subject_id = SelectField('Subject', coerce=int, validators=[Optional()])
    price = DecimalField('Price', validators=[Optional()])
    billing_rate = DecimalField('Billing Rate', validators=[Optional()])
    payrate = DecimalField('Pay Rate', validators=[Optional()])
    registration_start = DateField('Registration Start', validators=[Optional()])
    registration_end = DateField('Registration End', validators=[Optional()])
    class_start = DateField('Class Start', validators=[Optional()])
    class_end = DateField('Class End', validators=[Optional()])
    class_time_start = TimeField('Time Class Start', validators=[Optional()])
    class_time_end = TimeField('Time Class End', validators=[Optional()])
    grade_limit_from = IntegerField('Grade Limit From', validators=[Optional()])
    grade_limit_to = IntegerField('Grade Limit To', validators=[Optional()])
    age_limit_from = IntegerField('Age Limit From', validators=[Optional()])
    age_limit_to = IntegerField('Age Limit To', validators=[Optional()])
    info = TextAreaField('Class Description', validators=[Optional()])
    day_of_week = StringField('Day of Week', validators=[Optional()])
    current = BooleanField('Current Class', validators=[Optional()])
    submit = SubmitField('Update')
