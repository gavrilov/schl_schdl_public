from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Optional


class SubjectForm(FlaskForm):
    name = StringField(_l('Name of Subject'), validators=[DataRequired()])
    current = BooleanField(_l('Current Subject'))
    color = StringField(_l('Color'), validators=[Optional()])
    default_info = TextAreaField(_l('Default Class Description'), validators=[Optional()])
    # password = StringField(_l('Password'), validators=[DataRequired()])
    # email = StringField(_l('Email'), validators=[DataRequired()])
    # easypost_api_key = StringField(_l('EasyPost API Key'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
