from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional


class UserForm(FlaskForm):
    first_name = StringField(_l('First Name'), validators=[DataRequired(_l('Please enter your First Name'))])
    last_name = StringField(_l('Last Name'), validators=[DataRequired(_l('Please enter your Last Name'))])
    email = StringField(_l('Email'), validators=[Optional()])
    submit = SubmitField(_l('Submit'))
