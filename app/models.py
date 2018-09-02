from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import login
from app.database import db


class Schdl_Class(db.Model):
    __tablename__ = "classes"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    current = db.Column('current', db.Boolean())
    events = db.relationship('Event', backref='schl_class', lazy='dynamic')


class School(db.Model):
    __tablename__ = "schools"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.Unicode(2048))
    director_name = db.Column('director_name', db.Unicode(2048))
    note = db.Column('note', db.Unicode(2048))
    current = db.Column('current', db.Boolean())
    classes = db.relationship('Schdl_Class', backref='school', lazy='dynamic')
    contacts = db.relationship('SchoolContacts', backref='school', lazy='dynamic')


class SchoolContacts(db.Model):
    __tablename__ = "schoolcontacts"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    note = db.Column('note', db.Unicode(2048))
    email = db.Column('email', db.Unicode(2048))
    phone = db.Column('phone', db.Unicode(2048), index=True)
    address1 = db.Column('address1', db.Unicode(2048))
    address2 = db.Column('address2', db.Unicode(2048))
    city = db.Column('city', db.Unicode(2048))
    state = db.Column('state', db.Unicode(2048))
    zip = db.Column('zip', db.Unicode(2048))


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.Unicode(2048))
    current = db.Column('current', db.Boolean())
    classes = db.relationship('Schdl_Class', backref='subject', lazy='dynamic')


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column('first_name', db.Unicode(2048))
    last_name = db.Column('last_name', db.Unicode(2048))
    current = db.Column('current', db.Boolean())
    classes = db.relationship('Schdl_Class', backref='teacher', lazy='dynamic')
    events = db.relationship('Event', backref='teacher', lazy='dynamic')
    contacts = db.relationship('TeacherContacts', backref='teacher', lazy='dynamic')


class TeacherContacts(db.Model):
    __tablename__ = "teachercontacts"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    note = db.Column('note', db.Unicode(2048))
    email = db.Column('email', db.Unicode(2048))
    phone = db.Column('phone', db.Unicode(2048), index=True)
    address1 = db.Column('address1', db.Unicode(2048))
    address2 = db.Column('address2', db.Unicode(2048))
    city = db.Column('city', db.Unicode(2048))
    state = db.Column('state', db.Unicode(2048))
    zip = db.Column('zip', db.Unicode(2048))


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    # school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    username = db.Column('username', db.Unicode(2048), unique=True, index=True)
    first_name = db.Column('first_name', db.Unicode(2048))
    last_name = db.Column('last_name', db.Unicode(2048))
    students = db.relationship('Student', backref='user', lazy='dynamic')
    contacts = db.relationship('UserContacts', backref='user', lazy='dynamic')
    password_hash = db.Column(db.Unicode(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserContacts(db.Model):
    __tablename__ = "usercontacts"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    note = db.Column('note', db.Unicode(2048))
    email = db.Column('email', db.Unicode(2048))
    phone = db.Column('phone', db.Unicode(2048), index=True)
    address1 = db.Column('address1', db.Unicode(2048))
    address2 = db.Column('address2', db.Unicode(2048))
    city = db.Column('city', db.Unicode(2048))
    state = db.Column('state', db.Unicode(2048))
    zip = db.Column('zip', db.Unicode(2048))


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column('first_name', db.Unicode(2048))
    last_name = db.Column('last_name', db.Unicode(2048))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # classes = db.relationship('Schdl_Class', backref='teacher', lazy='dynamic')
    # events = db.relationship('Event', backref='teacher', lazy='dynamic')
