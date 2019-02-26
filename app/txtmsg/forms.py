from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional
from wtforms.widgets import TextArea


class TxtMsgForm(FlaskForm):
    phone_number = StringField(_l('Phone Numbers'), validators=[Optional()], widget=TextArea())
    msg = StringField(_l('Message'), validators=[Optional()], widget=TextArea())
    note = StringField(_l('Note'), validators=[Optional()])
    # upload = FileField(_l('Image'), validators=[FileAllowed(['jpg', 'png'], _l('Images only!'))])
    submit = SubmitField(_l('Send!'))
