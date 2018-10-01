from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Optional


class ClassForm(FlaskForm):
    school_id = SelectField('School', coerce=int, validators=[Optional()])
    teacher_id = SelectField('Teacher', coerce=int, validators=[Optional()])
    subject_id = SelectField('Subject', coerce=int, validators=[Optional()])
    price = DecimalField('Price', validators=[DataRequired()])
    info = TextAreaField('Class Description')
    current = BooleanField('Current Class')
    submit = SubmitField('Update')

