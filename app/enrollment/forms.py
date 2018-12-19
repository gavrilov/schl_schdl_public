from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField, BooleanField
from wtforms.validators import DataRequired, Optional


class EnrollmentForm(FlaskForm):
    id = HiddenField(_l('id'), validators=[Optional()])
    student_id = HiddenField(_l('Student id'), validators=[DataRequired()])
    class_id = SelectField(_l('Class'), coerce=int, validators=[Optional()])
    note = StringField(_l('Note'), validators=[Optional()])
    current = BooleanField(_l('Current'), validators=[Optional()])
    submit = SubmitField(_l('Submit'))
