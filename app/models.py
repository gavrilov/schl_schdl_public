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

# table many-to-many connects classes and teachers (one class has few user teachers. one teacher may have few classes)
classes_teacher = db.Table('classes_teacher', db.Column('teacher_id', db.Integer(), db.ForeignKey('teachers.id')),
                           db.Column('class_id', db.Integer(), db.ForeignKey('classes.id')))


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    text = db.Column('text', db.Unicode(2048))


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    timestamp_last_change = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    note = db.Column('note', db.Unicode(2048))
    current = db.Column('current', db.Boolean())


class Schdl_Class(db.Model):
    __tablename__ = "classes"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    # teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'))
    current = db.Column('current', db.Boolean())
    info = db.Column('info', db.UnicodeText())
    day_of_week = db.Column('day_of_week', db.Unicode(2048))
    price = db.Column('price', db.Numeric(scale=2))
    events = db.relationship('Event', backref='schdl_class', lazy='dynamic', cascade="all, delete-orphan")
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
    short_name = db.Column('short_name', db.Unicode(2048))
    type = db.Column('type', db.Unicode(2048))
    director_name = db.Column('director_name', db.Unicode(2048))
    note = db.Column('note', db.Unicode(2048))
    hide_from_users = db.Column('hide_from_users', db.Boolean(), default=False)
    current = db.Column('current', db.Boolean())
    agreement = db.Column('agreement', db.UnicodeText())
    classes = db.relationship('Schdl_Class', backref='school', lazy='dynamic')


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.Unicode(2048))
    name_es = db.Column('name_es', db.Unicode(2048))
    color = db.Column('color', db.Unicode(32))
    current = db.Column('current', db.Boolean())
    default_info = db.Column('default_info', db.UnicodeText())  # default description will insert to Schdl_Class.info
    classes = db.relationship('Schdl_Class', backref='subject', lazy='dynamic')
    awards = db.relationship('Award', backref='subject', lazy='dynamic')


class Semester(db.Model):
    __tablename__ = "semesters"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.Unicode(2048))
    color = db.Column('color', db.Unicode(32))
    current = db.Column('current', db.Boolean())
    classes = db.relationship('Schdl_Class', backref='semester', lazy='dynamic')
    show_in_list = db.Column('show_in_list', db.Boolean(), default=False)  #show in default list for students


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    note = db.Column('note', db.Unicode(2048))
    current = db.Column('current', db.Boolean(), default=False)
    classes = db.relationship('Schdl_Class', secondary=classes_teacher, backref='teachers', lazy='dynamic')
    events = db.relationship("Payroll", back_populates="teacher")
    # payrolls = db.relationship('Payroll', backref='teacher', lazy='dynamic')
    read_only = db.Column('read_only', db.Boolean(), default=False)
    # classes = db.relationship('Schdl_Class', backref='teacher', lazy='dynamic')
    # events = db.relationship('Event', backref='teacher', lazy='dynamic')


class Payroll(db.Model):
    __tablename__ = "payrolls"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    payrate = db.Column('payrate', db.Numeric(scale=2))
    note = db.Column('note', db.Unicode(2048))
    paid = db.Column('current', db.Boolean(), default=False)

    teacher = db.relationship('Teacher', back_populates="events")
    event = db.relationship('Event', back_populates="teachers")


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    note = db.Column('note', db.Unicode(2048))
    event_note = db.Column('event_note', db.Unicode(2048))
    active = db.Column('active', db.Boolean())
    payrate = db.Column('payrate', db.Numeric(scale=2))
    billing_rate = db.Column('billing_rate', db.Numeric(scale=2))
    start = db.Column('start', db.DateTime(timezone=True))
    end = db.Column('end', db.DateTime(timezone=True))
    teachers = db.relationship('Payroll', back_populates="event", lazy='dynamic', cascade="all, delete-orphan")
    attendances = db.relationship('Attendance', backref='event', lazy='dynamic', cascade="all, delete-orphan")


class Attendance(db.Model):
    __tablename__ = "attendances"
    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    status = db.Column('status', db.Integer())  # 1 - for A, 2 - for P
    note = db.Column('note', db.Unicode(2048))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


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
    dont_want_back = db.Column('dont_want_back', db.Boolean(), default=False)


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
    notes = db.relationship('Note', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    default_school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    attendances = db.relationship('Attendance', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    awards = db.relationship('StudentAwards', backref='student', lazy='dynamic', cascade="all, delete-orphan")
    dont_want_back = db.Column('dont_want_back', db.Boolean(), default=False)


class Award(db.Model):
    __tablename__ = "awards"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode(2048))
    rank = db.Column('rank', db.Integer)
    note = db.Column('note', db.Unicode(2048))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    awards_records = db.relationship('StudentAwards', backref='award', lazy='dynamic')


class StudentAwards(db.Model):
    __tablename__ = "student_awards"
    id = db.Column('id', db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    award_id = db.Column(db.Integer, db.ForeignKey('awards.id'))
    date = db.Column('date', db.DateTime, default=datetime.datetime.utcnow)
    note = db.Column('note', db.Unicode(2048))


# for Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
