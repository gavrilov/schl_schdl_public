import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate

from app.database import db
from config import Config

migrate = Migrate()
login = LoginManager()
login.login_view = 'user.sing_in'
login.login_message = 'Please log in to access this page.'
login.login_message_category = "warning"


def create_app(config_class=Config):
    app = Flask(__name__)
    Bootstrap(app)
    login.init_app(app)
    login.login_view = 'user.sign_in'
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']

    #====== BLUEPRINTS ========================================================
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

    if not app.debug and not app.testing:
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

        app.logger.setLevel(logging.INFO)
        app.logger.info('App startup')


    @app.route('/')
    def hello_world():
        return redirect(url_for('user.email_check'))

    db.init_app(app)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app is while within this block
        db.create_all()

    migrate.init_app(app, db)
    return app

