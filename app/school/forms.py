from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Optional, ValidationError
from flask import flash


def selection_validator(form, field):
    if field.data == 0 or field.data == '0':
        flash('You have not selected {} '.format(field.label.text), 'danger')
        raise ValidationError('You have not selected {} '.format(field.label.text))


class SchoolForm(FlaskForm):
    name = StringField('School Name', validators=[DataRequired()])
    director_name = StringField('Director Name', validators=[Optional()])
    note = StringField('Note', validators=[Optional()])
    agreement = StringField('Additional Agreement for Parents', validators=[Optional()])
    type = SelectField('Type',
                        choices=[('0', '---'), ('PP/CC', 'PP/CC'), ('PP/EC', 'PP/EC')],
                        validators=[selection_validator])
    current = BooleanField('Current School')
    # password = StringField('Password', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired()])
    # easypost_api_key = StringField('EasyPost API Key', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SchoolListForm(FlaskForm):
    school_id = SelectField('School', coerce=int, validators=[Optional()])
    submit = SubmitField('Submit')
