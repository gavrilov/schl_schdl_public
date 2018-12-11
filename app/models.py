import datetime

from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# table many-to-many connects users and roles secondary=roles_users
roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

# table many-to-many connects users and schools (one school has few user accounts. one user may have few schools)
schools_users = db.Table('schools_users', db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                         db.Column('school_id', db.Integer(), db.ForeignKey('schools.id')))


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    note = db.Column('note', db.Unicode(2048))
    current = db.Column('current', db.Boolean())


class Schdl_Class(db.Model):
    __tablename__ = "classes"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    current = db.Column('current', db.Boolean())
    info = db.Column('info', db.UnicodeText())
    day_of_week = db.Column('day_of_week', db.Unicode(2048))
    price = db.Column('price', db.Numeric(scale=2))
    events = db.relationship('Event', backref='schdl_class', lazy='dynamic')
    registration_start = db.Column('registration_start', db.DateTime)
    registration_end = db.Column('registration_end', db.DateTime)
    grade_limit_from = db.Column('grade_limit_from', db.Integer)
    grade_limit_to = db.Column('grade_limit_to', db.Integer)
    age_limit_from = db.Column('age_limit_from', db.Integer)
    age_limit_to = db.Column('age_limit_to', db.Integer)
    billing_rate = db.Column('billing_rate', db.Numeric(scale=2))
    payrate = db.Column('payrate', db.Numeric(scale=2))
    class_start = db.Column('class_start', db.DateTime)
    class_end = db.Column('class_end', db.DateTime)
    class_time_start = db.Column('class_time_start', db.Time)
    class_time_end = db.Column('class_time_end', db.Time)
    enrollments = db.relationship('Enrollment', backref='schdl_class', lazy='dynamic')
    # default_students = db.relationship('Student', backref='default_school', lazy='dynamic')


class School(db.Model):
    __tablename__ = "schools"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.Unicode(2048))
    type = db.Column('type', db.Unicode(2048))
    director_name = db.Column('director_name', db.Unicode(2048))
    note = db.Column('note', db.Unicode(2048))
    current = db.Column('current', db.Boolean())
    agreement = db.Column('agreement', db.UnicodeText())
    classes = db.relationship('Schdl_Class', backref='school', lazy='dynamic')


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.Unicode(2048))
    color = db.Column('color', db.Unicode(32))
    current = db.Column('current', db.Boolean())
    default_info = db.Column('default_info', db.UnicodeText())  # default description will insert to Schdl_Class.info
    classes = db.relationship('Schdl_Class', backref='subject', lazy='dynamic')


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    note = db.Column('note', db.Unicode(2048))
    current = db.Column('current', db.Boolean())
    classes = db.relationship('Schdl_Class', backref='teacher', lazy='dynamic')
    events = db.relationship('Event', backref='teacher', lazy='dynamic')


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    note = db.Column('note', db.Unicode(2048))
    active = db.Column('active', db.Boolean())
    payrate = db.Column('payrate', db.Numeric(scale=2))
    billing_rate = db.Column('billing_rate', db.Numeric(scale=2))
    start = db.Column('start', db.DateTime)
    end = db.Column('end', db.DateTime)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    stripe_id = db.Column('stripe_id', db.Unicode(2048))
    email = db.Column('email', db.Unicode(2048), unique=True, index=True)
    first_name = db.Column('first_name', db.Unicode(2048))
    last_name = db.Column('last_name', db.Unicode(2048))
    password = db.Column('password', db.Unicode(2048))
    active = db.Column('active', db.Boolean())
    confirmed_at = db.Column('confirmed_at', db.DateTime())
    students = db.relationship('Student', backref='user', lazy='dynamic')
    schools = db.relationship('School', secondary=schools_users, backref='users', lazy='dynamic')
    teachers = db.relationship('Teacher', backref='user', lazy='dynamic')
    contacts = db.relationship('UserContacts', backref='user', lazy='dynamic')
    note = db.Column('note', db.Unicode(2048))
    roles = db.relationship('Role', secondary=roles_users, backref='users', lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"
    id = db.Column('id', db.Integer(), primary_key=True)
    name = db.Column('name', db.String(80), unique=True)
    description = db.Column('description', db.String(255))


class UserContacts(db.Model):
    __tablename__ = "usercontacts"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    nickname = db.Column('nickname', db.Unicode(2048))
    note = db.Column('note', db.Unicode(2048))
    email = db.Column('email', db.Unicode(2048))
    phone = db.Column('phone', db.Unicode(2048), index=True)
    address1 = db.Column('address1', db.Unicode(2048))
    address2 = db.Column('address2', db.Unicode(2048))
    city = db.Column('city', db.Unicode(2048))
    state = db.Column('state', db.Unicode(2048))
    zip = db.Column('zip', db.Unicode(2048))
    contact_by_email = db.Column('contact_by_email', db.Boolean())
    contact_by_txt = db.Column('contact_by_txt', db.Boolean())
    contact_by_mail = db.Column('contact_by_mail', db.Boolean())


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column('first_name', db.Unicode(2048))
    last_name = db.Column('last_name', db.Unicode(2048))
    gender = db.Column('gender', db.Integer())  # 1 - for boy, 2 - for girl
    grade = db.Column('grade', db.Integer())  # -3 for preschools, -2 for PreK, -1 for K, 1-12 regular
    dob = db.Column('dob', db.DateTime)
    note = db.Column('note', db.Unicode(2048))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    default_school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


# for Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
