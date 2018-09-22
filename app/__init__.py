import logging
import os
from logging.handlers import RotatingFileHandler

from SlackLogger import SlackHandler
from flask import Flask, redirect, url_for, render_template, abort
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from flask_security import Security, utils
from raven.contrib.flask import Sentry

from app.models import db, user_datastore
from app.user.forms import SignInForm, RegistrationForm
from config import Config

security = Security()
migrate = Migrate()
sentry = Sentry()
bootstrap = Bootstrap()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']

    bootstrap.init_app(app)
    security.init_app(app, user_datastore, login_form=SignInForm, register_form=RegistrationForm)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    #====== BLUEPRINTS ========================================================
    from app.admin.views import admin
    app.register_blueprint(admin, url_prefix='/dashboard')
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
    # ====== END-BLUEPRINTS ===================================================

    # Logging for Production
    if not app.debug and not app.testing:
        # Heroku logging
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/schl_schdl.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        # Slack logging
        slack_handler = SlackHandler(app.config['SLACK_WEBHOOK_URL'])
        slack_handler.setLevel(logging.INFO)
        app.logger.addHandler(slack_handler)

        # Sentry.io logging
        sentry.init_app(app, logging=True, level=logging.WARNING)

        app.logger.setLevel(logging.INFO)
        app.logger.info('App startup')

    @app.route('/')
    def hello_world():
        return redirect(url_for('security.register'))

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
            user_datastore.create_user(email=app.config['SUPERADMIN'], password=encrypted_password)

            db.session.commit()

            user_datastore.add_role_to_user(app.config['SUPERADMIN'], 'superadmin')
            user_datastore.add_role_to_user(app.config['SUPERADMIN'], 'admin')
            user_datastore.add_role_to_user(app.config['SUPERADMIN'], 'school')
            user_datastore.add_role_to_user(app.config['SUPERADMIN'], 'teacher')
            db.session.commit()

            return redirect(url_for('user.main'))
        else:
            return abort(404)

    return app
