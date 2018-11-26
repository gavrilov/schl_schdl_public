from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Optional, ValidationError


def selection_validator(form, field):
    if field.data == 0 or field.data == '0':
        raise ValidationError("You have not selected type of school")


class SchoolForm(FlaskForm):
    name = StringField('School Name', validators=[DataRequired()])
    director_name = StringField('Director Name', validators=[Optional()])
    note = StringField('Note', validators=[Optional()])
    type = SelectField('Type',
                        choices=[(0, '---'), (1, 'PP/CC'), (2, 'PP/EC')],
                        validators=[selection_validator])
    current = BooleanField('Current School')
    # password = StringField('Password', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired()])
    # easypost_api_key = StringField('EasyPost API Key', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SchoolListForm(FlaskForm):
    school_id = SelectField('School', coerce=int, validators=[Optional()])
    submit = SubmitField('Submit')
