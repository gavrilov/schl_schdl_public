from flask import render_template, Blueprint, current_app, redirect, url_for, flash
from flask_security import current_user, roles_required

from app import db
from app.admin.forms import UserForm
from app.models import School, Teacher, Subject, Schdl_Class, Event, User, Student  # , Role

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def main():
    current_app.logger.info("Admin {} has been signed in to admin console".format(current_user.email))
    return render_template('admin/dashboard.html')


@admin.route('/school', methods=['GET', 'POST'])
@roles_required('admin')
def school_list():
    schools = School.query.filter_by(current=True).all()
    return render_template('admin/school_list.html', schools=schools, current_schools_only=True)


@admin.route('/teacher', methods=['GET', 'POST'])
@roles_required('admin')
def teacher_list():
    teachers = Teacher.query.filter_by(current=True).all()
    return render_template('admin/teacher_list.html', teachers=teachers, current_steachers_only=True)


@admin.route('/subject', methods=['GET', 'POST'])
@roles_required('admin')
def subject_list():
    subjects = Subject.query.filter_by(current=True).all()
    return render_template('admin/subject_list.html', subjects=subjects)


@admin.route('/class', methods=['GET', 'POST'])
@roles_required('admin')
def class_list():
    classes = Schdl_Class.query.filter_by(current=True).all()
    return render_template('admin/class_list.html', classes=classes, current_classes_only=True)


@admin.route('/event', methods=['GET', 'POST'])
@roles_required('admin')
def event_list():
    events = Event.query.filter_by().all()
    # TODO current_events_only - by date or Schdl_Class.current = True. if today in range(start_date_of_class, end_date_of_class)
    return render_template('admin/event_list.html', events=events, current_events_only=False)


@admin.route('/user', methods=['GET', 'POST'])
@roles_required('admin')
def user_list():
    # users = Role.query.filter_by(name='admin').first().users  # admins only
    users = User.query.all()
    return render_template('admin/user_list.html', users=users)


@admin.route('/students', methods=['GET', 'POST'])
@roles_required('admin')
def student_list():
    students = Student.query.all()
    return render_template('admin/student_list.html', students=students)
