import re

from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from flask_babelex import _
from flask_security import roles_required
from flask_security import url_for_security
from twilio.rest import Client

from app.models import UserContacts
from app.txtmsg.forms import TxtMsgForm, ResetTxtMsgForm

txtmsg = Blueprint('txtmsg', __name__, template_folder='templates')


@txtmsg.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def send_msg():
    form = TxtMsgForm()

    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_AUTH_TOKEN']
    messaging_ssid = current_app.config['TWILIO_MESSAGING_SSID']

    client = Client(account_sid, auth_token)

    to_phone = request.args.get('to_phone')
    phone_numbers = request.args.get('phone_numbers')
    txt_messages = None
    if to_phone:
        form.phone_number.data = to_phone
        txt_messages = client.messages.page(to=to_phone, page_size=10)
        # print(txt_messages.__dict__)
    if phone_numbers:
        phone_numbers = str(phone_numbers).replace(',', '\r\n')
        form.phone_number.data = phone_numbers

    if form.validate_on_submit():
        # check if the post request has the file part
        # TODO Add file to txt msg
        """ 
        if form.upload:
            file = form.upload.data
            if file is not None:
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                media_url = str(DOMAIN_URL) + str(url_for('txtmsg.uploaded_file',
                                                          filename=filename))
                """

        # get a list with standard numbers
        phone_numbs = str(form.phone_number.data).replace('"', '').replace(' ', '').replace('-', '').replace('\r',
                                                                                                             '').replace(
            '/', '\n').split('\n')
        text_message = form.msg.data
        note = form.note.data

        for number in phone_numbs:
            if number is not "" and len(number) == 10:
                message = client.messages.create(
                    messaging_service_sid=messaging_ssid,
                    body=text_message,
                    to=number,
                    media_url=url_for('static', filename='default_txt_media.png', _external=True, _scheme='https')
                )
                try:
                    status = message.status
                    msgid = message.sid
                except:
                    flash(message.error_message, 'danger')
                    pass
            else:
                flash(_('Number {phone_number} is wrong').format(phone_number=number), 'danger')

        return redirect(url_for('txtmsg.status'))
    else:
        return render_template('txtmsg/sms_form.html', form=form, txt_messages=txt_messages, to_phone=to_phone)


@txtmsg.route('/status', methods=['GET', 'POST'])
@roles_required('admin')
def status():
    page = 0
    page_token = None

    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('page_token'):
        page_token = str(request.args.get('page_token'))

    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_AUTH_TOKEN']
    messaging_ssid = current_app.config['TWILIO_MESSAGING_SSID']

    client = Client(account_sid, auth_token)

    txt_messages = client.messages.page(page_size=25, page_number=page, page_token=page_token)
    return render_template('txtmsg/sms_status.html', data=txt_messages, page=page)


@txtmsg.route('/updatestatus', methods=['POST'])
def sms_status_callback():
    # it is a callback url. Twillo makes requests with status updates
    message_sid = request.form['MessageSid']
    message_status = request.form['MessageStatus']
    return render_template('page.html'), 200


@txtmsg.route('/forgot_email', methods=['GET', 'POST'])
def forgot_email():
    form = ResetTxtMsgForm()
    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_AUTH_TOKEN']
    messaging_ssid = current_app.config['TWILIO_MESSAGING_SSID']

    client = Client(account_sid, auth_token)

    if form.validate_on_submit():
        # TODO logger that

        phone_number = re.sub("\D", "", form.phone_number.data)

        # find contact with phone number and text user email or reset link
        contact = UserContacts.query.filter_by(phone=phone_number).first()
        if not contact:
            flash(_('Account with this phone number does not find. Please call office if you have questions'), 'danger')
            return render_template('security/forgot_email.html', forgot_email_form=form)

        text_message = _("You can use {email} to login. If you do not remember password reset it here: {reset_url}").format(email=contact.user.email, reset_url=url_for_security('forgot_password', _external=True, _scheme='https'))
        note = _('Reset email txt msg')

        if phone_number is not "" and len(phone_number) == 10:
            message = client.messages.create(
                messaging_service_sid=messaging_ssid,
                body=text_message,
                to=phone_number,
                media_url=url_for('static', filename='default_txt_media.png', _external=True, _scheme='https')
            )
            try:
                status = message.status
                msgid = message.sid
            except:
                flash(message.error_message, 'danger')
                pass
            flash(_('Text message has been send'), 'success')
        else:
            flash(_('Number {phone_number} is wrong').format(phone_number=phone_number), 'danger')

        return redirect(url_for_security('login'))
    else:
        return render_template('security/forgot_email.html', forgot_email_form=form)
