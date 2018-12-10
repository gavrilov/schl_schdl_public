from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import Optional


class TeacherForm(FlaskForm):
    note = StringField(_l('Note'), validators=[Optional()])
    current = BooleanField(_l('Current Teacher'))
    submit = SubmitField(_l('Submit'))
