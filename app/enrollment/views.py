from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_babelex import _
from flask_security import roles_required, current_user
from .forms import EnrollmentForm
from app.models import User, Student, Teacher, Enrollment, Schdl_Class, School, Semester
from app import db
import datetime

enrollment = Blueprint('enrollment', __name__, template_folder='templates')


@enrollment.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def list_all():

    page = request.args.get('page', 1, type=int)
    enrollments = Enrollment.query.order_by(Enrollment.timestamp.desc()).paginate(page, 20, False)

    next_url = url_for('enrollment.list_all', page=enrollments.next_num) \
        if enrollments.has_next else None
    prev_url = url_for('enrollment.list_all', page=enrollments.prev_num) \
        if enrollments.has_prev else None

    return render_template('enrollment/list.html', enrollments=enrollments.items, next_url=next_url, prev_url=prev_url)


@enrollment.route('/current', methods=['GET', 'POST'])
@roles_required('admin')
def list_current():
    # Dashboard for teachers
    enrollments = Enrollment.query.filter_by(current=True).all()
    return 'Hello from Current Enrollments'  # render_template('', enrollments=enrollments)


@enrollment.route('/add/<student_id>', methods=['GET', 'POST'])
@roles_required('admin')
def add(student_id):
    form = EnrollmentForm()
    current_classes = Schdl_Class.query.filter_by(current=True).join(Semester, Schdl_Class.semester).filter_by(current=True).order_by(Semester.name.asc()).join(School, Schdl_Class.school).order_by(School.name.asc()).all()

    class_list = [(i.id, i.semester.name + " - " + i.school.name + '@' + i.subject.name + ' ' + i.day_of_week + ' ' + (
        i.class_time_start.strftime("%I:%M %p") if i.class_time_start else "")) for i in current_classes]
    form.class_id.choices = class_list

    if form.validate_on_submit():
        form.id.data = None
        current_student = Student.query.filter_by(id=student_id).first()
        new_enrollment = Enrollment()
        form.populate_obj(new_enrollment)
        current_student.enrollments.append(new_enrollment)
        db.session.commit()
        flash(_('New Enrollment created'), 'success')
        return redirect(url_for('student.info', student_id=current_student.id))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(err)
        form.student_id.data = student_id
        return render_template('enrollment/modal_add_enrolment.html', form=form)


@enrollment.route('/edit/<enrollment_id>', methods=['GET', 'POST'])
@roles_required('admin')
def edit(enrollment_id):

    current_classes = Schdl_Class.query.filter_by(current=True).join(Semester, Schdl_Class.semester).order_by(Semester.name.asc()).join(School, Schdl_Class.school).order_by(School.name.asc()).all()
    current_enrollment = Enrollment.query.filter_by(id=enrollment_id).first()
    form = EnrollmentForm(obj=current_enrollment)
    class_list = [(i.id, i.semester.name + " - " + i.school.name + '@' + i.subject.name + ' ' + i.day_of_week + ' ' + (i.class_time_start.strftime("%I:%M %p") if i.class_time_start else "")) for i in current_classes]
    form.class_id.choices = class_list
    if form.validate_on_submit():
        form.populate_obj(current_enrollment)
        current_enrollment.timestamp_last_change = datetime.datetime.utcnow()  # uncomment if you want to save time of last change
        db.session.commit()
        flash(_('Enrollment has been updated'), 'success')
        return redirect(url_for('student.info', student_id=current_enrollment.student_id))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(err)
        return render_template('enrollment/modal_edit_enrolment.html', form=form)


@enrollment.route('/delete/<enrollment_id>', methods=['GET', 'POST'])
@roles_required('admin')
def delete(enrollment_id):

    current_enrollment = Enrollment.query.filter_by(id=enrollment_id).first()
    current_student = current_enrollment.student
    if current_enrollment:
        db.session.delete(current_enrollment)
        db.session.commit()
        flash(_('Enrollment has been deleted'), 'success')
        return redirect(url_for('student.info', student_id=current_student.id))
    else:
        flash(_('Enrollment did not find'), 'danger')
        return redirect(url_for('student.info', student_id=current_student.id))
