from flask_security.forms import RegisterForm, LoginForm
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, InputRequired, Optional, Regexp


class SignInForm(LoginForm):
    recaptcha = RecaptchaField()


class RegistrationForm(RegisterForm):
    first_name = StringField('First Name', validators=[DataRequired("Please enter your First Name")])
    last_name = StringField('Last Name', validators=[DataRequired("Please enter your Last Name")])
    agreement = BooleanField('I agree to the Terms of Service and Privacy Policy',
                             validators=[DataRequired("You must accept the agreement to continue")])
    recaptcha = RecaptchaField()


class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired("Please enter your First Name")])
    last_name = StringField('Last Name', validators=[DataRequired("Please enter your Last Name")])
    submit = SubmitField('Submit')


class UserContactForm(FlaskForm):
    # TODO validate: email? address info with USPS, phone number
    email = EmailField("Email", validators=[InputRequired("Please enter your email address")])
    phone = StringField('Cellphone #', validators=[DataRequired("Please enter your phone number"),
                                                   Regexp("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$",
                                                          message="Please enter 10 digits of your Cellphone number i.e. 83212345678")])
    address1 = StringField('Mailing Address', validators=[DataRequired("Please enter your address")])
    address2 = StringField('Address 2', validators=[Optional()])
    city = StringField('City', validators=[DataRequired("Please enter your City")])
    state = SelectField('State', validators=[DataRequired("Please enter your State")],
                        choices=[("AL", "Alabama"), ("AK", "Alaska"), ("AS", "American Samoa"), ("AZ", "Arizona"),
                                 ("AR", "Arkansas"), ("CA", "California"), ("CO", "Colorado"), ("CT", "Connecticut"),
                                 ("DE", "Delaware"), ("DC", "District Of Columbia"),
                                 ("FM", "Federated States Of Micronesia"), ("FL", "Florida"), ("GA", "Georgia"),
                                 ("GU", "Guam"), ("HI", "Hawaii"), ("ID", "Idaho"), ("IL", "Illinois"),
                                 ("IN", "Indiana"), ("IA", "Iowa"), ("KS", "Kansas"), ("KY", "Kentucky"),
                                 ("LA", "Louisiana"), ("ME", "Maine"), ("MH", "Marshall Islands"), ("MD", "Maryland"),
                                 ("MA", "Massachusetts"), ("MI", "Michigan"), ("MN", "Minnesota"),
                                 ("MS", "Mississippi"), ("MO", "Missouri"), ("MT", "Montana"), ("NE", "Nebraska"),
                                 ("NV", "Nevada"), ("NH", "New Hampshire"), ("NJ", "New Jersey"), ("NM", "New Mexico"),
                                 ("NY", "New York"), ("NC", "North Carolina"), ("ND", "North Dakota"),
                                 ("MP", "Northern Mariana Islands"), ("OH", "Ohio"), ("OK", "Oklahoma"),
                                 ("OR", "Oregon"), ("PW", "Palau"), ("PA", "Pennsylvania"), ("PR", "Puerto Rico"),
                                 ("RI", "Rhode Island"), ("SC", "South Carolina"), ("SD", "South Dakota"),
                                 ("TN", "Tennessee"), ("TX", "Texas"), ("UT", "Utah"), ("VT", "Vermont"),
                                 ("VI", "Virgin Islands"), ("VA", "Virginia"), ("WA", "Washington"),
                                 ("WV", "West Virginia"), ("WI", "Wisconsin"), ("WY", "Wyoming")])
    zip = StringField('ZIP', validators=[DataRequired("Please enter your ZIP code"), Regexp("^\d{5}(?:[-\s]\d{4})?$",
                                                                                            message="Please enter 5 digit of your ZIP code i.e 77001")])
    contact_by_email = BooleanField('email', validators=[Optional()])
    contact_by_txt = BooleanField('text messages', validators=[Optional()])
    contact_by_mail = BooleanField('mail', validators=[Optional()])
    note = StringField('Note', validators=[Optional()])
    submit = SubmitField('Submit')