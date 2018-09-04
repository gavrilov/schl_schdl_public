from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo, Optional


class EmailCheckForm(FlaskForm):
    username = EmailField("Email", validators=[InputRequired("Please enter your email address."),
                                               Email("Please enter your email address.")])
    recaptcha = RecaptchaField()
    submit = SubmitField('Next')


class SignInForm(FlaskForm):
    username = EmailField("Email", validators=[InputRequired("Please enter your email address."),
                                               Email("Please enter your email address.")])
    password = PasswordField("Password", validators=[DataRequired("Please enter your password")])
    remember_me = BooleanField('Keep me signed in')
    recaptcha = RecaptchaField()
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = EmailField("Email", validators=[InputRequired("Please enter your email address."),
                                               Email("Please enter your email address.")])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserContactForm(FlaskForm):
    # TODO validate: email? address info with USPS, phone number
    email = EmailField("Email", validators=[InputRequired("Please enter your email address."),
                                            Email("Please enter your email address.")])
    phone = StringField('Cellphone #', validators=[DataRequired()])
    address1 = StringField('Address 1', validators=[DataRequired()])
    address2 = StringField('Address 2', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', validators=[DataRequired()],
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
    zip = StringField('ZIP', validators=[DataRequired()])
    note = StringField('Note', validators=[Optional()])
    submit = SubmitField('Submit')