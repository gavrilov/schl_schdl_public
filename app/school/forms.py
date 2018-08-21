from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Optional


class SchoolForm(FlaskForm):
    school_name = StringField('School Name', validators=[DataRequired()])
    current = BooleanField('Current School')
    #password_hash = StringField('Password', validators=[DataRequired()])
    #email = StringField('Email', validators=[DataRequired()])
    #easypost_api_key = StringField('EasyPost API Key', validators=[DataRequired()])
    submit = SubmitField('Submit')

""" # Delete 
class EasypostDefaultAddressForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    street1 = StringField('street1', validators=[DataRequired()])
    street2 = StringField('street2', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    zip = StringField('ZIP', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EasypostShipmentForm(FlaskForm):
    from_first_name = StringField('First Name', validators=[Optional()])
    from_last_name = StringField('Last Name', validators=[Optional()])
    from_company = StringField('Company', validators=[Optional()])
    from_street1 = StringField('Street 1', validators=[DataRequired()])
    from_street2 = StringField('Street 2', validators=[Optional()])
    from_city = StringField('City', validators=[DataRequired()])
    from_state = StringField('State', validators=[DataRequired()])
    from_country = StringField('Country', validators=[DataRequired()])
    from_zip = StringField('ZIP', validators=[DataRequired()])
    from_phone = StringField('Phone Number', validators=[DataRequired()])
    to_first_name = StringField('First Name', validators=[Optional()])
    to_last_name = StringField('Last Name', validators=[Optional()])
    to_company = StringField('Company', validators=[Optional()])
    to_street1 = StringField('Street 1', validators=[DataRequired()])
    to_street2 = StringField('Street 2', validators=[Optional()])
    to_city = StringField('City', validators=[DataRequired()])
    to_state = StringField('State', validators=[DataRequired()])
    to_country = StringField('Country', validators=[DataRequired()])
    to_zip = StringField('ZIP', validators=[DataRequired()])
    to_phone = StringField('Phone Number', validators=[DataRequired()])
    weight_lbs = StringField('lbs', validators=[DataRequired()], default=0)
    weight_oz = StringField('oz', validators=[DataRequired()], default=0)
    length = StringField('Length', validators=[Optional()])
    width = StringField('Width', validators=[Optional()])
    height = StringField('Height', validators=[Optional()])
    easypost_users = SelectField('User', coerce=int, validators=[Optional()])
    insurance = StringField('Insurance', validators=[Optional()], default=0)
    submit = SubmitField('Submit')


class EasypostRatesForm(FlaskForm):
    service = SelectField('Service', coerce=int, validators=[Optional()])
    submit = SubmitField('Buy Label')
"""