import os
from dotenv import load_dotenv

load_dotenv() 
#Config file

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ES config
    COMPANY_NAME = os.environ.get('COMPANY_NAME')
    COMPANY_LOGO_URL = os.environ.get('COMPANY_LOGO_URL')
    COMPANY_SLOGAN = os.environ.get('COMPANY_SLOGAN')
    COMPANY_CONTACT_PHONE = os.environ.get('COMPANY_CONTACT_PHONE')
    COMPANY_CONTACT_EMAIL = os.environ.get('COMPANY_CONTACT_EMAIL')
    LANGUAGES = os.environ.get('LANGUAGES')
    SUPERADMIN = os.environ.get('SUPERADMIN')
    BOOTSTRAP_SERVE_LOCAL = os.environ.get('BOOTSTRAP_SERVE_LOCAL')
    STATIC_FOLDER = os.path.join(basedir, 'static')
    # Secret key for signing cookies
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = os.environ.get('CSRF_ENABLED')
    # Use a secure, unique and absolutely secret key for signing the data.
    CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY')

    # DB Settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    DATABASE_CONNECT_OPTIONS = os.environ.get('DATABASE_CONNECT_OPTIONS')

    # Heroku logger output
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # Application threads. A common general assumption is using 2 per available processor cores - to handle incoming requests using one and performing background operations using the other.
    THREADS_PER_PAGE = os.environ.get('THREADS_PER_PAGE')

    # RECAPTCHA Settings
    RECAPTCHA_DATA_ATTRS = os.environ.get('RECAPTCHA_DATA_ATTRS')
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_PARAMETERS = os.environ.get('RECAPTCHA_PARAMETERS')

    # Slack webhook for error logging
    SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

    CURRENT_RELEASE_VERSION = os.environ.get('CURRENT_RELEASE_VERSION') or 'current release'
    CURRENT_RELEASE_CREATED_AT = os.environ.get('CURRENT_RELEASE_CREATED_AT') or 'current date'
    CURRENT_RELEASE_HEROKU_VERSION = os.environ.get('CURRENT_RELEASE_HEROKU_VERSION') or 'current version'

    # Sentery.io dsn
    SENTRY_CONFIG = os.environ.get('SENTRY_CONFIG')
    SENTRY_USER_ATTRS = os.environ.get('SENTRY_USER_ATTRS')

    # Flask-Security Settings
    SECURITY_REGISTERABLE = os.environ.get('SECURITY_REGISTERABLE')
    SECURITY_RECOVERABLE = os.environ.get('SECURITY_RECOVERABLE')
    SECURITY_CHANGEABLE = os.environ.get('SECURITY_CHANGEABLE')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_PASSWORD_HASH = os.environ.get('SECURITY_PASSWORD_HASH')
    SECURITY_POST_LOGIN_VIEW = os.environ.get('SECURITY_POST_LOGIN_VIEW')
    SECURITY_POST_REGISTER_VIEW = os.environ.get('SECURITY_POST_REGISTER_VIEW')
    SECURITY_MSG_UNAUTHORIZED = ('You do not have permission to view this resource', 'danger')
    # Email Server Settings
    SPARKPOST_API_KEY = os.environ.get('SPARKPOST_API_KEY')
    SECURITY_SEND_REGISTER_EMAIL = os.environ.get('SECURITY_SEND_REGISTER_EMAIL')  # send email confirmation
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Stripe production settings
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

    # Twilio test settings
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_MESSAGING_SSID = os.environ.get('TWILIO_MESSAGING_SSID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_DEFAULT_ANSWER = os.environ.get('TWILIO_DEFAULT_ANSWER')
    NOTE_FOR_ALL_PARENTS = os.environ.get('NOTE_FOR_ALL_PARENTS')
    AGREEMENT = os.environ.get('AGREEMENT')
