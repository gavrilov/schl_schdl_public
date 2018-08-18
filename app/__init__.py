from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from .database import db

migrate = Migrate()


def create_app(config_filename):
    app = Flask(__name__)
    Bootstrap(app)

    app.config.from_pyfile(config_filename)
    app.secret_key = app.config['SECRET_KEY']

    #====== BLUEPRINTS ========================================================
    from app.school.views import school
    app.register_blueprint(school, url_prefix='/school')

    # ====== END-BLUEPRINTS ===================================================

    @app.route('/')
    def hello_world():
        return render_template('main_page.html')

    db.init_app(app)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app is while within this block
        db.create_all()

    migrate.init_app(app, db)
    return app

