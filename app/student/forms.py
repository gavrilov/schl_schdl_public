from flask import flash
from flask_babelex import _
from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Optional, ValidationError


def selection_validator(form, field):
    if field.data == 0 or field.data == '0':
        flash(_('You have not selected {field_label}').format(field_label=field.label.text), 'danger')
        raise ValidationError(_('You have not selected {field_label}').format(field_label=field.label.text))


class StudentForm(FlaskForm):
    first_name = StringField(_l('Student First Name'),
                             validators=[DataRequired(_l('Please enter First Name of Student'))])
    last_name = StringField(_l('Student Last Name'),
                            validators=[DataRequired(_l('Please enter your Last Name of Student'))])
    gender = SelectField(_l('Gender'), choices=[('0', '---'), ('1', _l('Boy')), ('2', _l('Girl'))],
                         validators=[selection_validator])
    dob = DateField(_l('Student Date of Birth'), validators=[Optional()])
    dob_month = SelectField(_l('Month'),
                            choices=[('0', _l('Month')), ('01', _l('01 - Jan')), ('02', _l('02 - Feb')),
                                     ('03', _l('03 - Mar')),
                                     ('04', _l('04 - Apr')), ('05', _l('05 - May')), ('06', _l('06 - Jun')),
                                     ('07', _l('07 - Jul')),
                                     ('08', _l('08 - Aug')), ('09', _l('09 - Sep')), ('10', _l('10 - Oct')),
                                     ('11', _l('11 - Nov')),
                                     ('12', _l('12 - Dec'))], validators=[selection_validator])
    dob_day = SelectField(_l('Day'),
                          choices=[('0', _l('Day')), ('01', '1'), ('02', '2'), ('03', '3'), ('04', '4'), ('05', '5'),
                                   ('06', '6'), ('07', '7'), ('08', '8'), ('09', '9'), ('10', '10'), ('11', '11'),
                                   ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'),
                                   ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'),
                                   ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'),
                                   ('30', '30'), ('31', '31')], validators=[selection_validator])
    dob_year = SelectField(_l('Year'), choices=[('0', _l('Year')), ('2004', '2004'), ('2005', '2005'), ('2006', '2006'),
                                                ('2007', '2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'),
                                                ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'),
                                                ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'),
                                                ('2019', '2019'), ('2020', '2020')],
                           validators=[selection_validator])
    default_school_id = SelectField(_l('School'), coerce=int, validators=[selection_validator])
    grade = SelectField(_l('Grade'), choices=[(0, '---'), (-3, _l('Preschool')), (-2, _l('Pre-Kindergarten')),
                                              (-1, _l('Kindergarten')),
                                              (1, _l('1st')), (2, _l('2nd')), (3, _l('3rd')), (4, _l('4th')),
                                              (5, _l('5th')), (6, _l('6th')), (7, _l('7th'))], coerce=int,
                        validators=[selection_validator])
    submit = SubmitField(_l('Submit'))


class StudentFormDashboard(StudentForm):
    dont_want_back = BooleanField(_l('Dont want back'), validators=[Optional()])
