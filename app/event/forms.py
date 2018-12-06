from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional


class PopupEventForm(FlaskForm):
    id = StringField('id', validators=[Optional()])
    payrate = StringField('Payrate', validators=[Optional()])
    billing_rate = StringField('Billing Rate', validators=[Optional()])
    datetime_start = StringField('Date time start', validators=[Optional()])
    datetime_end = StringField('Date time end', validators=[Optional()])
    note = StringField('note', validators=[Optional()])
    class_id = StringField('Class', validators=[Optional()])
    active = StringField('Active', validators=[Optional()])
    submit = SubmitField('Update')
