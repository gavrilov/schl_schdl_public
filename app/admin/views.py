from flask import render_template, Blueprint, redirect, url_for, current_app
from flask_login import current_user, login_required

from app.models import School, Teacher, Subject, Schdl_Class, Event, User, Student

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/', methods=['GET', 'POST'])
@login_required
def main():
    if current_user.email not in current_app.config['ADMIN_USERNAME']:
        current_app.logger.warning(
            "User {} with id = {} is trying to get admin access".format(current_user.email, current_user.id))
        return redirect(url_for('user.main'))
    current_app.logger.info("Admin {} has been signed in to admin console".format(current_user.email))
    return render_template('admin/dashboard.html')


@admin.route('/school', methods=['GET', 'POST'])
def school_list():
    schools = School.query.filter_by(current=True).all()
    return render_template('admin/school_list.html', schools=schools, current_schools_only=True)


@admin.route('/teacher', methods=['GET', 'POST'])
def teacher_list():
    teachers = Teacher.query.filter_by(current=True).all()
    return render_template('admin/teacher_list.html', teachers=teachers, current_steachers_only=True)


@admin.route('/subject', methods=['GET', 'POST'])
def subject_list():
    subjects = Subject.query.filter_by(current=True).all()
    return render_template('admin/subject_list.html', subjects=subjects)


@admin.route('/class', methods=['GET', 'POST'])
def class_list():
    classes = Schdl_Class.query.filter_by(current=True).all()
    return render_template('admin/class_list.html', classes=classes, current_classes_only=True)


@admin.route('/event', methods=['GET', 'POST'])
def event_list():
    events = Event.query.filter_by().all()
    # TODO current_events_only - by date or Schdl_Class.current = True. if today in range(start_date_of_class, end_date_of_class)
    return render_template('admin/event_list.html', events=events, current_events_only=False)


@admin.route('/user', methods=['GET', 'POST'])
def user_list():
    users = User.query.all()
    return render_template('admin/user_list.html', users=users)


@admin.route('/students', methods=['GET', 'POST'])
def student_list():
    students = Student.query.all()
    return render_template('admin/student_list.html', students=students)
