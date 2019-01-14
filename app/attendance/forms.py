from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, Optional


class AttendanceForm(FlaskForm):
    # id = HiddenField(_l('id'), validators=[Optional()])
    student_id = HiddenField(_l('Student id'), validators=[DataRequired()])
    event_id = HiddenField(_l('Event id'), validators=[DataRequired()])
    status = SelectField(_l('Status'), coerce=int, choices=[(0, '---'), (1, 'A'), (2, 'P')], validators=[Optional()])
    note = StringField(_l('Note'), validators=[Optional()])
    submit = SubmitField(_l('Submit'))
