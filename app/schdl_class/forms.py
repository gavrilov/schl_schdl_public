from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField, BooleanField, TextAreaField, IntegerField, StringField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import Optional


class ClassForm(FlaskForm):
    school_id = SelectField(_l('School'), coerce=int, validators=[Optional()])
    teacher_id = SelectField(_l('Teacher'), coerce=int, validators=[Optional()])
    subject_id = SelectField(_l('Subject'), coerce=int, validators=[Optional()])
    price = DecimalField(_l('Price'), validators=[Optional()])
    billing_rate = DecimalField(_l('Billing Rate'), validators=[Optional()])
    payrate = DecimalField(_l('Pay Rate'), validators=[Optional()])
    registration_start = DateField(_l('Registration Start'), validators=[Optional()])
    registration_end = DateField(_l('Registration End'), validators=[Optional()])
    class_start = DateField(_l('Class Start'), validators=[Optional()])
    class_end = DateField(_l('Class End'), validators=[Optional()])
    class_time_start = TimeField(_l('Time Class Start'), validators=[Optional()])
    class_time_end = TimeField(_l('Time Class End'), validators=[Optional()])
    grade_limit_from = IntegerField(_l('Grade Limit From'), validators=[Optional()])
    grade_limit_to = IntegerField(_l('Grade Limit To'), validators=[Optional()])
    age_limit_from = IntegerField(_l('Age Limit From'), validators=[Optional()])
    age_limit_to = IntegerField(_l('Age Limit To'), validators=[Optional()])
    info = TextAreaField(_l('Class Description'), validators=[Optional()])
    day_of_week = StringField(_l('Day of Week'), validators=[Optional()])
    current = BooleanField(_l('Current Class'), validators=[Optional()])
    submit = SubmitField(_l('Update'))
