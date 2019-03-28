import logging
import os
from logging.handlers import RotatingFileHandler

import stripe
from flask import Flask, redirect, url_for, render_template, abort, flash, request, send_from_directory, current_app
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_security import Security, utils
from raven.contrib.flask import Sentry

from app.models import db, user_datastore, Schdl_Class, User, UserContacts
from app.user.forms import SignInForm, RegistrationForm
from config import Config
from .cli import register as cli

security = Security()
migrate = Migrate()
sentry = Sentry()
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
babel = Babel()

from flask_security import current_user
import datetime


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']
    cli(app)  # add babel translate command for command line
    bootstrap.init_app(app)
    security_ctx = security.init_app(app, user_datastore, login_form=SignInForm, register_form=RegistrationForm)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    babel.init_app(app)
    # ====== BLUEPRINTS ========================================================
    from app.dashboard.views import dashboard
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    from app.school.views import school
    app.register_blueprint(school, url_prefix='/school')
    from app.teacher.views import teacher
    app.register_blueprint(teacher, url_prefix='/teacher')
    from app.subject.views import subject
    app.register_blueprint(subject, url_prefix='/subject')
    from app.schdl_class.views import schdl_class
    app.register_blueprint(schdl_class, url_prefix='/class')
    from app.calendar.views import calendar
    app.register_blueprint(calendar, url_prefix='/calendar')
    from app.event.views import event
    app.register_blueprint(event, url_prefix='/event')
    from app.user.views import user
    app.register_blueprint(user, url_prefix='/user')
    from app.student.views import student
    app.register_blueprint(student, url_prefix='/student')
    from app.payment.views import payment
    app.register_blueprint(payment, url_prefix='/payment')
    from app.enrollment.views import enrollment
    app.register_blueprint(enrollment, url_prefix='/enrollment')
    from app.attendance.views import attendance
    app.register_blueprint(attendance, url_prefix='/attendance')
    from app.txtmsg.views import txtmsg
    app.register_blueprint(txtmsg, url_prefix='/txtmsg')
    # ====== END-BLUEPRINTS ===================================================

    # Logging for Production
    if not app.debug and not app.testing:
        # Heroku logging
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.WARNING)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/schl_schdl.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.WARNING)
            app.logger.addHandler(file_handler)

        # Sentry.io logging
        sentry.init_app(app, logging=True, level=logging.WARNING)

        app.logger.setLevel(logging.WARNING)
        app.logger.info('App startup')

    @app.route('/')
    def hello_world():
        return redirect(url_for('security.register'))

    @app.route('/import_stripe_addresses')
    def import_stripe_addresses():
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        users = User.query.all()
        for this_user in users:
            if this_user.stripe_id:
                try:
                    customer = stripe.Customer.retrieve(this_user.stripe_id)
                    if customer:
                        for card in customer['sources']['data']:
                            address = UserContacts()
                            if card.address_line1 and card.address_city and card.address_zip and card.address_state:
                                address.address1 = card.address_line1
                                address.address2 = card.address_line2
                                address.city = card.address_city
                                address.state = card.address_state
                                address.zip = card.address_zip
                                address.nickname = "stripe"
                                address.user_id = this_user.id
                            db.session.add(address)
                    db.session.commit()
                except:
                    current_app.logger.error('ADDRESS: User with id {} - address_error'.format(this_user.id))

        return 'ok'


    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')

    @app.route('/setup', methods=['GET', 'POST'])
    def setup():
        # run it once when move to new server - it creates roles and superadmin
        if not user_datastore.get_user(app.config['SUPERADMIN']):
            user_datastore.find_or_create_role(name='superadmin', description='Super Administrator')
            user_datastore.find_or_create_role(name='admin', description='Administrator')
            user_datastore.find_or_create_role(name='school', description='School')
            user_datastore.find_or_create_role(name='teacher', description='Teacher')

            encrypted_password = utils.hash_password('password')
            user_datastore.create_user(email=app.config['SUPERADMIN'], password=encrypted_password, first_name='First', last_name='Last')

            db.session.commit()

            user_datastore.add_role_to_user(app.config['SUPERADMIN'], 'superadmin')
            user_datastore.add_role_to_user(app.config['SUPERADMIN'], 'admin')
            user_datastore.add_role_to_user(app.config['SUPERADMIN'], 'school')
            user_datastore.add_role_to_user(app.config['SUPERADMIN'], 'teacher')
            db.session.commit()

            return redirect(url_for('user.main'))
        else:
            return abort(404)

    @app.template_filter('ctime')
    def timectime(s):
        # jinja2 template to convert unix timestamp to datetime object as required by flask-moment
        return datetime.datetime.utcfromtimestamp(s)

    @app.template_filter('ctimeformat')
    def timeformat(s):
        m = '{:%I:%M %p}'.format(s)
        # m = datetime.datetime.strptime(s, '%H:%M:%S').strftime('%h:%M %p')
        # jinja2 template to convert unix timestamp to datetime object as required by flask-moment
        return m

    @app.template_filter('cdateformat')
    def dateformat(s):
        m = '{:%m/%d/%Y}'.format(s)
        # m = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        # jinja2 template to convert unix timestamp to datetime object as required by flask-moment
        return m

    # To know when user visited web site last time
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.datetime.utcnow()
            db.session.commit()

    # Flexible way for defining custom mail sending task.
    # TODO try to switch to original SparkPost python lib
    @security_ctx.send_mail_task
    def send_email(msg):
        import requests
        msg_sender = str(msg.sender)
        msg_subject = str(msg.subject)
        msg_html = str(msg.html)
        msg_recipients = []
        for email in msg.recipients:
            msg_recipients.append(dict(address=dict(email=email)))
        url = 'https://api.sparkpost.com/api/v1/transmissions'
        spark_api_key = app.config['SPARKPOST_API_KEY']
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
                app.logger.error('SparkPost {} error: {}'.format(error['code'], error['message']))

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(app.config['LANGUAGES'])
        # return 'ru'  # to test specific language of babel

    @app.errorhandler(404)
    def page_not_found(e):
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            user_id = 'anonymous'
        app.logger.warning('Error 404 - User id = {}, url = {}'.format(user_id, request.url))
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('errors/500.html'), 500

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    return app
