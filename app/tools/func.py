import requests
import stripe
from flask import current_app, flash

from app.models import db, User, UserContacts, Enrollment


def send_email_to_user(user, msg_subject, msg_html):
    msg_sender = current_app.config['MAIL_DEFAULT_SENDER']
    msg_recipients_list = [user.email]
    msg_recipients = []
    for email in msg_recipients_list:
        msg_recipients.append(dict(address=dict(email=email)))
    url = 'https://api.sparkpost.com/api/v1/transmissions'
    spark_api_key = current_app.config['SPARKPOST_API_KEY']
    payload = {
        'recipients': msg_recipients,
        'content': {
            'from': msg_sender,
            'subject': msg_subject,
            'html': msg_html
        }
    }
    response = requests.post(url, headers={'Authorization': spark_api_key}, json=payload)
    r = response.json()
    if 'errors' in r:
        for error in r['errors']:
            flash("".format(error['message']), 'danger')
            current_app.logger.error('SparkPost {} error: {}'.format(error['code'], error['message']))
            return False
    return True


def import_stripe_addresses():
    # func to sync contact information from stripe to system
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    users = User.query.all()
    for this_user in users:
        if this_user.stripe_id:
            try:
                customer = stripe.Customer.retrieve(this_user.stripe_id)
                if customer:
                    for card in customer['sources']['data']:
                        address = UserContacts()

                        # check for duplicates
                        not_dup = True
                        for contact in this_user.contacts:
                            if card.address_line1 == contact.address1:
                                print('Dup find')
                                not_dup = False

                        if card.address_line1 and card.address_city and card.address_zip and card.address_state and not_dup:
                            address.address1 = card.address_line1
                            if card.address_line2:
                                address.address2 = card.address_line2
                            address.city = card.address_city
                            address.state = card.address_state
                            address.zip = card.address_zip
                            address.nickname = "stripe"
                            address.user_id = this_user.id
                        db.session.add(address)
                db.session.commit()
                print("USER ID {}".format(this_user.id))
            except:
                print("ERROR! USER ID {}".format(this_user.id))
                print(customer)
                current_app.logger.error('ADDRESS: User with id {} - address_error'.format(this_user.id))
                pass

    return 'ok'


def export_contacts():
    # def to export contacts to csv file
    enrollments = Enrollment.query.all()
    text = []
    for this_enrollment in enrollments:
        for contact in this_enrollment.student.user.contacts:
            address = "{student_first_name}\t{student_last_name}\t{school}\t{subject}\t{email}\t{phone}\t{address1}\t{address2}\t{city}\t{state}\t{zip}".format(
                student_first_name=this_enrollment.student.first_name,
                student_last_name=this_enrollment.student.last_name,
                school=this_enrollment.schdl_class.school.name,
                subject=this_enrollment.schdl_class.subject.name,
                email=contact.email,
                phone=contact.phone,
                address1=contact.address1,
                address2=contact.address2,
                city=contact.city,
                state=contact.state,
                zip=contact.zip
            )
            text.append(address)

    with open('csvfile.csv', 'w') as file:
        for line in text:
            file.write(line)
            file.write('\n')

    return 'Ok'


def contact_fixer():
    #fix phone numbers
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
