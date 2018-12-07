from flask import render_template, Blueprint
from flask_security import roles_accepted, roles_required

calendar = Blueprint('calendar', __name__, template_folder='templates')


# TODO @roles_accepted('admin', 'teacher') if user don't have access to event - hide


@calendar.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def main():
    # calendar for all classes at all schools
    return render_template('calendar/caledar.html', id='all', schdl_object='class')


@calendar.route('/class/<class_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def class_calendar(class_id):
    return render_template('calendar/caledar.html', id=class_id, schdl_object='class')


@calendar.route('/student/<student_id>', methods=['GET', 'POST'])
def student_calendar(student_id):
    return render_template('calendar/caledar.html', id=student_id, schdl_object='student')


@calendar.route('/user/<user_id>', methods=['GET', 'POST'])
def user_calendar(user_id):
    return render_template('calendar/caledar.html', id=user_id, schdl_object='user')


@calendar.route('/teacher/<teacher_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def teacher_calendar(teacher_id):
    return render_template('calendar/caledar.html', id=teacher_id, schdl_object='teacher')


@calendar.route('/school/<school_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'school')
def school_calendar(school_id):
    return render_template('calendar/class_caledar.html', id=school_id, schdl_object='school')
