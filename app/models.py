from app.database import db


class Schdl_Class(db.Model):
    __tablename__ = "classes"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('easypost_users.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    current = db.Column('current', db.Boolean())
    events = db.relationship('Event', backref='schl_class', lazy='dynamic')


class School(db.Model):
    __tablename__ = "schools"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.Unicode(2048))
    current = db.Column('current', db.Boolean())
    classes = db.relationship('Schdl_Class', backref='school', lazy='dynamic')
    #events = db.relationship('Event', backref='school', lazy='dynamic')
    #director_name = db.Column('director_name', db.Unicode(2048))
    #email = db.Column('email', db.Unicode(2048))
    #email2 = db.Column('email2', db.Unicode(2048))
    #phone1 = db.Column('phone1', db.Unicode(2048))
    #phone2 = db.Column('phone2', db.Unicode(2048))
    #website = db.Column('website', db.Unicode(2048))
    #addresses = db.relationship('EasypostDefaultAddress', backref='user', lazy='dynamic')


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.Unicode(2048))
    current = db.Column('current', db.Boolean())
    classes = db.relationship('Schdl_Class', backref='subject', lazy='dynamic')
    #director_name = db.Column('director_name', db.Unicode(2048))
    #email = db.Column('email', db.Unicode(2048))
    #email2 = db.Column('email2', db.Unicode(2048))
    #phone1 = db.Column('phone1', db.Unicode(2048))
    #phone2 = db.Column('phone2', db.Unicode(2048))
    #website = db.Column('website', db.Unicode(2048))
    #addresses = db.relationship('EasypostDefaultAddress', backref='user', lazy='dynamic')


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column('first_name', db.Unicode(2048))
    last_name = db.Column('last_name', db.Unicode(2048))
    current = db.Column('current', db.Boolean())
    classes = db.relationship('Schdl_Class', backref='teacher', lazy='dynamic')
    events = db.relationship('Event', backref='teacher', lazy='dynamic')
    #director_name = db.Column('director_name', db.Unicode(2048))
    #email = db.Column('email', db.Unicode(2048))
    #email2 = db.Column('email2', db.Unicode(2048))
    #phone1 = db.Column('phone1', db.Unicode(2048))
    #phone2 = db.Column('phone2', db.Unicode(2048))
    #website = db.Column('website', db.Unicode(2048))
    #addresses = db.relationship('EasypostDefaultAddress', backref='user', lazy='dynamic')


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    # school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))


class Parent(db.Model):
    __tablename__ = "parents"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column('first_name', db.Unicode(2048))
    last_name = db.Column('last_name', db.Unicode(2048))

    #classes = db.relationship('Schdl_Class', backref='teacher', lazy='dynamic')
    #events = db.relationship('Event', backref='teacher', lazy='dynamic')