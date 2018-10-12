from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField, BooleanField, TextAreaField
from wtforms.validators import Optional


class ClassForm(FlaskForm):
    school_id = SelectField('School', coerce=int, validators=[Optional()])
    teacher_id = SelectField('Teacher', coerce=int, validators=[Optional()])
    subject_id = SelectField('Subject', coerce=int, validators=[Optional()])
    price = DecimalField('Price', validators=[Optional()])
    info = TextAreaField('Class Description', validators=[Optional()])
    current = BooleanField('Current Class', validators=[Optional()])
    submit = SubmitField('Update')

