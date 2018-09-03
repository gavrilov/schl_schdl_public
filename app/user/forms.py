from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, BooleanField, PasswordField
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
    remember_me = BooleanField('Remember Me')
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
    state = StringField('State', validators=[DataRequired()])
    zip = StringField('ZIP', validators=[DataRequired()])
    note = StringField('Note', validators=[Optional()])
    submit = SubmitField('Submit')