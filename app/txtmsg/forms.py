from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea
from wtforms.fields import TelField
from wtforms.validators import DataRequired, Optional, Regexp


class TxtMsgForm(FlaskForm):
    phone_number = StringField(_l('Phone Numbers'), validators=[Optional()], widget=TextArea())
    msg = StringField(_l('Message'), validators=[Optional()], widget=TextArea())
    note = StringField(_l('Note'), validators=[Optional()])
    # upload = FileField(_l('Image'), validators=[FileAllowed(['jpg', 'png'], _l('Images only!'))])
    submit = SubmitField(_l('Send!'))


class ResetTxtMsgForm(FlaskForm):
    phone_number = TelField(_l('Cellphone #'), validators=[DataRequired(_l('Please enter your phone number')),
                                                           Regexp("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$",
                                                                  message=_l(
                                                                      'Please enter 10 digits of your Cellphone number i.e. 83212345678'))])
    submit = SubmitField(_l('Send text msg!'))
