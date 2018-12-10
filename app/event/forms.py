from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import Optional


class PopupEventForm(FlaskForm):
    payrate = StringField('Payrate', validators=[Optional()])
    billing_rate = StringField('Billing Rate', validators=[Optional()])
    start = DateTimeField('Date time start', validators=[Optional()], format='%m/%d/%Y %I:%M %p')
    end = DateTimeField('Date time end', validators=[Optional()], format='%m/%d/%Y %I:%M %p')
    note = StringField('Note', validators=[Optional()])
    class_id = StringField('Class id', validators=[Optional()])
    teacher_id = SelectField('Teacher', coerce=int, validators=[Optional()])
    active = BooleanField('Active', validators=[Optional()])
    submit = SubmitField('Update')
