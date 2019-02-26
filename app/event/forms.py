from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import Optional


class PopupEventForm(FlaskForm):
    payrate = StringField(_l('Payrate'), validators=[Optional()])
    billing_rate = StringField(_l('Billing Rate'), validators=[Optional()])
    start = DateTimeField(_l('Date time start'), validators=[Optional()], format='%m/%d/%Y %I:%M %p')
    end = DateTimeField(_l('Date time end'), validators=[Optional()], format='%m/%d/%Y %I:%M %p')
    note = StringField(_l('Note'), validators=[Optional()])
    event_note = StringField(_l('Event Note'), validators=[Optional()])
    # class_id = StringField(_l('Class id'), validators=[Optional()])
    # teacher_id = SelectField(_l('Teacher'), coerce=int, validators=[Optional()])
    active = BooleanField(_l('Active'), validators=[Optional()])
    submit = SubmitField(_l('Update'))
