import requests
from flask import current_app


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
