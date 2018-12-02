from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional, ValidationError


def selection_validator(form, field):
    if field.data == 0 or field.data == '0':
        flash('You have not selected {} '.format(field.label.text), 'danger')
        raise ValidationError('You have not selected {} '.format(field.label.text))


class StudentForm(FlaskForm):
    first_name = StringField('Student First Name', validators=[DataRequired("Please enter First Name of Student")])
    last_name = StringField('Student Last Name', validators=[DataRequired("Please enter your Last Name of Student")])
    gender = SelectField('Gender', choices=[('0', '---'), ('1', 'Boy'), ('2', 'Girl')], validators=[selection_validator])
    dob = DateField('Student Date of Birth', validators=[Optional()])
    dob_month = SelectField('Month', choices=[('0', 'Month'), ('01', 'Jan'), ('02', 'Feb'), ('03', 'Mar'), ('04', 'Apr'), ('05', 'May'), ('06', 'Jun'), ('07', 'Jul'), ('08', 'Aug'), ('09', 'Sep'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')], validators=[selection_validator])
    dob_day = SelectField('Day', choices=[('0', 'Day'), ('01', '1'), ('02', '2'), ('03', '3'), ('04', '4'), ('05', '5'), ('06', '6'), ('07', '7'), ('08', '8'), ('09', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')], validators=[selection_validator])
    dob_year = SelectField('Year', choices=[('0', 'Year'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006'), ('2007', '2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018')], validators=[selection_validator])
    default_school_id = SelectField('School', coerce=int, validators=[selection_validator])
    grade = SelectField('Grade', choices=[(0, '---'), (-3, 'Preschool'), (-2, 'Pre-Kindergarten'), (-1, 'Kindergarten'),
                                          (1, '1st'), (2, '2nd'), (3, '3rd'), (4, '4th'), (5, '5th')], coerce=int,
                        validators=[selection_validator])
    submit = SubmitField('Submit')
