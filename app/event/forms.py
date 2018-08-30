from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, BooleanField
from wtforms.validators import DataRequired, Optional


class EventForm(FlaskForm):
    #school_id = SelectField('School', coerce=int, validators=[Optional()])
    teacher_id = SelectField('Teacher', coerce=int, validators=[Optional()])
    class_id = SelectField('Class', coerce=int, validators=[Optional()])
    # note = StringField('Description', validators=[DataRequired()])
    # current = BooleanField('Current Class')
    submit = SubmitField('Update')

