from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from flask_babelex import _
from flask_security import roles_required
from twilio.rest import Client
from flask_security import url_for_security

from app.models import db, TextMessage, UserContacts, User
from app.txtmsg.forms import TxtMsgForm, ResetTxtMsgForm
import re

txtmsg = Blueprint('txtmsg', __name__, template_folder='templates')


@txtmsg.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def send_msg():
    form = TxtMsgForm()
    to_phone = request.args.get('to_phone')
    if to_phone:
        form.phone_number.data = to_phone
    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_AUTH_TOKEN']
    messaging_ssid = current_app.config['TWILIO_MESSAGING_SSID']

    client = Client(account_sid, auth_token)

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
                txt_msg = TextMessage()
                txt_msg.msgid = msgid
                txt_msg.phone_number = number
                txt_msg.msg = text_message
                txt_msg.note = note
                txt_msg.status = status
                db.session.add(txt_msg)
                db.session.commit()
            else:
                flash(_('Number {phone_number} is wrong').format(phone_number=number), 'danger')

        return redirect(url_for('txtmsg.status'))
    else:
        return render_template('txtmsg/sms_form.html', form=form)


@txtmsg.route('/status', methods=['GET', 'POST'])
@roles_required('admin')
def status():
    page = 1
    if request.args.get('page'):
        page = int(request.args.get('page'))
    txt_msg = TextMessage.query.order_by(TextMessage.id.desc()).paginate(page, 25, False)
    return render_template('txtmsg/sms_status.html', data=txt_msg)


@txtmsg.route('/updatestatus', methods=['POST'])
def sms_status_callback():
    # it is a callback url. Twillo makes requests with status updates
    message_sid = request.form['MessageSid']
    message_status = request.form['MessageStatus']
    txt_msg = TextMessage.query.filter_by(msgid=message_sid).first()
    txt_msg.status = message_status
    db.session.commit()
    return render_template('page.html'), 200


@txtmsg.route('/contact_fixer', methods=['GET', 'POST'])
@roles_required('admin')
def contact_fixer():
    contacts = UserContacts.query.all()
    for contact in contacts:
        contact_changed = False
        # if not contact.email:
        #    contact.email = contact.user.email
        #    contact_changed = True

        if contact.phone:
            format_phone = re.sub("\D", "", contact.phone)
            if format_phone != contact.phone:
                contact.phone = format_phone
                contact_changed = True
        if contact_changed:
            db.session.commit()
    # q = db.session.query(User)
    # users = q.filter(~User.contacts.any()).all()  # ~ means not
    # for user in users:
    #    new_contact = UserContacts(user_id=user.id, email=user.email)
    #    db.session.add(new_contact)
    #    db.session.commit()
    return 'Ok'


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
            txt_msg = TextMessage()
            txt_msg.msgid = msgid
            txt_msg.phone_number = phone_number
            txt_msg.msg = text_message
            txt_msg.note = note
            txt_msg.status = status
            db.session.add(txt_msg)
            db.session.commit()
            flash(_('Text message has been send'), 'success')
        else:
            flash(_('Number {phone_number} is wrong').format(phone_number=phone_number), 'danger')

        return redirect(url_for_security('login'))
    else:
        return render_template('security/forgot_email.html', forgot_email_form=form)
