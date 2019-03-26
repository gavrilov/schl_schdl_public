import datetime

from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Optional


class StudentAwardForm(FlaskForm):
    student_id = HiddenField(_l('Student id'), validators=[DataRequired()])
    award_id = SelectField(_l('Award'), coerce=int, validators=[Optional()])
    date = DateTimeField(_l('Date'), validators=[Optional()], default=datetime.datetime.utcnow)
    note = StringField(_l('Note'), validators=[Optional()])
    submit = SubmitField(_l('Submit'))


class StudentEditAwardForm(StudentAwardForm):
    id = HiddenField(_l('id'), validators=[DataRequired()])


class AwardForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    rank = IntegerField(_l('Rank'), validators=[DataRequired()])
    note = StringField(_l('Note'), validators=[Optional()])
    subject_id = SelectField(_l('Subject'), coerce=int, validators=[Optional()])
    submit = SubmitField(_l('Submit'))


class AwardEditForm(AwardForm):
    id = HiddenField(_l('id'), validators=[DataRequired()])

