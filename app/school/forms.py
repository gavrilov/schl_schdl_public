from flask import flash
from flask_babelex import _
from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Optional, ValidationError


def selection_validator(form, field):
    if field.data == 0 or field.data == '0':
        flash(_('You have not selected %(field_label)s', field_label=field.label.text), 'danger')
        raise ValidationError(_('You have not selected %(field_label)s', field_label=field.label.text))


class SchoolForm(FlaskForm):
    name = StringField(_l('School Name'), validators=[DataRequired()])
    director_name = StringField(_l('Director Name'), validators=[Optional()])
    note = StringField(_l('Note'), validators=[Optional()])
    agreement = StringField(_l('Additional Agreement for Users'), validators=[Optional()])
    type = SelectField(_l('Type'),
                        choices=[('0', '---'), ('PP/CC', 'PP/CC'), ('PP/EC', 'PP/EC')],
                        validators=[selection_validator])
    current = BooleanField(_l('Current School'))
    # password = StringField(_l('Password'), validators=[DataRequired()])
    # email = StringField(_l('Email'), validators=[DataRequired()])
    # easypost_api_key = StringField(_l('EasyPost API Key'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class SchoolListForm(FlaskForm):
    school_id = SelectField(_l('School'), coerce=int, validators=[Optional()])
    submit = SubmitField(_l('Submit'))
