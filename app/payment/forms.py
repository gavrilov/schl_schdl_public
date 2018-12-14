from flask_babelex import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, HiddenField
from wtforms.validators import DataRequired


class PaymentForm(FlaskForm):
    user_id = HiddenField(validators=[DataRequired()])
    amount = DecimalField(_l('Amount'), validators=[DataRequired(_l('Please enter amount'))])
    description = StringField(_l('Description'), validators=[DataRequired(_l('Please enter description'))])
    submit = SubmitField(_l('Charge'))
