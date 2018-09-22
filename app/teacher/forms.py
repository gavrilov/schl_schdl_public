from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import Optional


class TeacherForm(FlaskForm):
    note = StringField('Note', validators=[Optional()])
    current = BooleanField('Current Teacher')
    submit = SubmitField('Submit')
