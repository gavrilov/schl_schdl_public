from flask import jsonify
from flask import render_template, Blueprint, flash, redirect, url_for
from flask_security import roles_required, roles_accepted, current_user
from flask_babelex import _

from app import db
from app.models import Attendance, Enrollment, Schdl_Class
from .forms import AttendanceForm

attendance = Blueprint('attendance', __name__, template_folder='templates')


@attendance.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def list_all():
    # Dashboard for teachers
    enrollments = Enrollment.query.all()
    return 'Hello from All attendance'  # render_template('', enrollments=enrollments)


@attendance.route('/class/<class_id>', methods=['GET', 'POST'])
@roles_accepted('teacher', 'admin', 'school')
def for_class(class_id):
    form = AttendanceForm()
    current_class = Schdl_Class.query.filter_by(id=class_id).first()
    if current_user.has_role('admin'):
        return render_template('attendance/class_attendance.html', current_class=current_class, form=form)
    elif current_user.has_role('teacher'):
        for teacher in current_user.teachers:
            if current_class in teacher.classes and not teacher.read_only:
                return render_template('attendance/class_attendance.html', current_class=current_class, form=form)
            elif current_class in teacher.classes and teacher.read_only:
                return render_template('attendance/school_class_attendance.html', current_class=current_class,
                                       form=form)
            else:
                flash(_('You do not have permission to get attendance for that class. Please contact office'), 'danger')
                return redirect(url_for('dashboard.teacher_dashboard'))
    elif current_user.has_role('school'):
        for school in current_user.schools:
            if current_class in school.classes:
                return render_template('attendance/school_class_attendance.html', current_class=current_class, form=form)
        # If current user dosent have access to school with that class - show flash
        flash(_('You do not have permission to get attendance for that class. Please contact office'), 'danger')
        return redirect(url_for('dashboard.school_dashboard'))



@attendance.route('/change', methods=['POST'])
@roles_accepted('teacher', 'admin')
def change():
    form = AttendanceForm()

    if form.validate_on_submit():
        resp = jsonify(success=True)
        resp.status_code = 200
        check_attendance = Attendance.query.filter_by(student_id=form.student_id.data,
                                                      event_id=form.event_id.data).first()
        if not check_attendance:
            # print('New attendance record')
            new_attendance = Attendance()
            form.populate_obj(new_attendance)
            # new_attendance.id = None
            db.session.add(new_attendance)
            db.session.commit()
        else:
            # print('Updating attendance with id', check_attendance.id)
            update_attendance = check_attendance
            form.populate_obj(update_attendance)

            db.session.commit()
        # print(form.student_id.data, form.event_id.data, form.status.data)
        return resp
    else:
        resp = jsonify(success=False)
        resp.status_code = 400
        # print(form.student_id.data, form.event_id.data, form.status.data)
        # print("Not Ok :(")
        return resp


@attendance.route('/get_data/<class_id>', methods=['POST', 'GET'])
@roles_accepted('teacher', 'admin', 'school')
def get_data(class_id):
    # TODO Check if user has permission to get attendance for class
    current_class = Schdl_Class.query.filter_by(id=class_id).first()
    current_enrollments = current_class.enrollments.filter_by(current=True).all()
    attendance_data = []
    for current_event in current_class.events:
        for current_attendance in current_event.attendances:
            for enrollment in current_attendance.student.enrollments:
                # if enrollment in current_enrollments: # uncomment for data of current students without drops
                attendance_data.append({'id': 's{}e{}'.format(current_attendance.student_id, current_event.id),
                                'status': current_attendance.status})
    # print(str(attendance_data))
    resp = jsonify(attendance_data)
    resp.status_code = 200
    return resp
