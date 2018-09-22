from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# table many-to-many conects users and roles secondary=roles_users
roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

schools_users = db.Table('schools_users', db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                         db.Column('school_id', db.Integer(), db.ForeignKey('schools.id')))


class Schdl_Class(db.Model):
    __tablename__ = "classes"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    current = db.Column('current', db.Boolean())
    events = db.relationship('Event', backref='schdl_class', lazy='dynamic')
    enrollments = db.relationship('Enrollment', backref='schdl_class', lazy='dynamic')


class School(db.Model):
    __tablename__ = "schools"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.Unicode(2048))
    director_name = db.Column('director_name', db.Unicode(2048))
    note = db.Column('note', db.Unicode(2048))
    current = db.Column('current', db.Boolean())
    classes = db.relationship('Schdl_Class', backref='school', lazy='dynamic')


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.Unicode(2048))
    current = db.Column('current', db.Boolean())
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
    # school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
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
    gender = db.Column('gender', db.Boolean())  # 1 - for boy, 0 - for girl
    dob = db.Column('dob', db.DateTime)
    note = db.Column('note', db.Unicode(2048))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic')
    # classes = db.relationship('Schdl_Class', backref='teacher', lazy='dynamic')


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))


# for Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
