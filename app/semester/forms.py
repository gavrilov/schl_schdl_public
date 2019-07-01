from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional


class SemesterForm(FlaskForm):
    name = StringField(_l('Name of Semester'), validators=[DataRequired()])
    current = BooleanField(_l('Current Semester'))
    show_in_list = BooleanField(_l('Show Students of that Semester in default Student List'))
    color = StringField(_l('Color'), validators=[Optional()])
    submit = SubmitField(_l('Submit'))
