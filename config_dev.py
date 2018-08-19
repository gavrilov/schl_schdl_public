# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = 'C:/Projects/schl_schdl/static/'
# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Projects/chl_schdl/app/database.db'
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for signing the data.
CSRF_SESSION_KEY = "Wtik8gBt1n5OdIwc3pmdnyCSIXWLYbDntpBC6SnRUGsd5RLWPL3KYegxHFnxgy2F"

# Secret key for signing cookies
SECRET_KEY = 'UVnH6ebcCvaJ669vvqojQyhh6DrDLTpRSyABGdEf1uBMqUytQcCzgh4ci9i4nEzE'

# Secret key for RECAPTCHA
# RECAPTCHA_PUBLIC_KEY = '6LfhXhMUAAAAALodysaBvIvAcN3pFuP6_43ndVgO'
# RECAPTCHA_PRIVATE_KEY = '6LfhXhMUAAAAALlQOeLsI3wLqGEYo5XID9E80tqd'
# RECAPTCHA_PARAMETERS = {'hl': 'ru'}
