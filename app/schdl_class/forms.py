from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, BooleanField
from wtforms.validators import DataRequired, Optional


class ClassForm(FlaskForm):
    school_id = SelectField('School', coerce=int, validators=[Optional()])
    teacher_id = SelectField('Teacher', coerce=int, validators=[Optional()])
    subject_id = SelectField('Subject', coerce=int, validators=[Optional()])
    #note = StringField('Description', validators=[DataRequired()])
    current = BooleanField('Current Class')
    submit = SubmitField('Update')

