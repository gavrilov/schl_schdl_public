from flask_babelex import lazy_gettext as _l
from flask_security.forms import RegisterForm, LoginForm
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired, Optional, Regexp


class SignInForm(LoginForm):
    recaptcha = RecaptchaField()


class RegistrationForm(RegisterForm):
    first_name = StringField(_l('First Name'), validators=[DataRequired(_l('Please enter your First Name'))])
    last_name = StringField(_l('Last Name'), validators=[DataRequired(_l('Please enter your Last Name'))])
    agreement = BooleanField(_l('I agree to the Terms of Service and Privacy Policy'),
                             validators=[DataRequired(_l('You must accept the agreement to continue'))])
    recaptcha = RecaptchaField()


class UserForm(FlaskForm):
    first_name = StringField(_l('First Name'), validators=[DataRequired(_l('Please enter your First Name'))])
    last_name = StringField(_l('Last Name'), validators=[DataRequired(_l('Please enter your Last Name'))])
    email = StringField(_l('Email'), validators=[DataRequired(_l('Please enter your Email'))])
    note = StringField(_l('Note'), validators=[Optional(_l('Please enter your Note'))])
    send_email = BooleanField(_l('Email an invitation'), validators=[Optional()], default=False)
    submit = SubmitField(_l('Submit'))


class UserSettingsForm(FlaskForm):
    first_name = StringField(_l('First Name'), validators=[DataRequired(_l('Please enter your First Name'))])
    last_name = StringField(_l('Last Name'), validators=[DataRequired(_l('Please enter your Last Name'))])
    submit = SubmitField(_l('Submit'))


class UserContactForm(FlaskForm):
    # TODO validate: email? address info with USPS, phone number
    # TODO Do we need email here? Delete it!
    email = EmailField(_l('Email'), validators=[Optional(_l('Please enter your email address'))])
    phone = TelField(_l('Cellphone #'), validators=[DataRequired(_l('Please enter your phone number')),
                                                    Regexp("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$",
                                                           message=_l(
                                                               'Please enter 10 digits of your Cellphone number i.e. 83212345678'))])
    address1 = StringField(_l('Mailing Address'), validators=[DataRequired(_l('Please enter your address'))])
    address2 = StringField(_l('Address 2'), validators=[Optional()])
    city = StringField(_l('City'), validators=[DataRequired(_l('Please enter your City'))])
    state = SelectField(_l('State'), validators=[DataRequired(_l('Please enter your State'))],
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
                                 ("WV", "West Virginia"), ("WI", "Wisconsin"), ("WY", "Wyoming")], default='TX')
    zip = StringField(_l('ZIP'),
                      validators=[DataRequired(_l('Please enter your ZIP code')), Regexp("^\d{5}(?:[-\s]\d{4})?$",
                                                                                         message=_l(
                                                                                             'Please enter 5 digit of your ZIP code i.e 77001'))])
    contact_by_email = BooleanField(_l('email'), validators=[Optional()])
    contact_by_txt = BooleanField(_l('text messages'), validators=[Optional()])
    contact_by_mail = BooleanField(_l('mail'), validators=[Optional()])
    note = StringField(_l('Note'), validators=[Optional()])
    submit = SubmitField(_l('Submit'))
