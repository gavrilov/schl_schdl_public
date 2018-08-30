from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
import os
import logging
from logging.handlers import RotatingFileHandler
from app.database import db
from config import Config
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    Bootstrap(app)

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
        return render_template('main_page.html')

    db.init_app(app)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app is while within this block
        db.create_all()

    migrate.init_app(app, db)
    return app

