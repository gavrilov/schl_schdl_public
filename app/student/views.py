from datetime import datetime

from flask import render_template, Blueprint, flash, redirect, url_for, current_app
from flask_babelex import _
from flask_security import current_user, login_required, roles_required
from sqlalchemy import and_

from app import db
from app.models import Student, Schdl_Class, School
from .forms import StudentForm

student = Blueprint('student', __name__, template_folder='templates')


@student.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def student_list():
    students_html = ""
    current_classes = Schdl_Class.query.filter_by(current=True).all()
    for current_class in current_classes:
        # generate rows for table for each class
        students_html += render_template('student/student_list_rows.html', current_class=current_class)
    return render_template('student/student_list.html', students_html=students_html, current_students_only=True)


@student.route('/all', methods=['GET', 'POST'])
@roles_required('admin')
def student_all_list():
    # show all students who enrolled in any classes or dropped
    students = Student.query.filter(Student.enrollments.any())
    return render_template('student/student_list_not_current.html', students=students)


@student.route('/not_enrolled', methods=['GET', 'POST'])
@roles_required('admin')
def not_enrolled():
    # show students who are not enrolled in any classes
    students = Student.query.filter(~Student.enrollments.any()).order_by(Student.timestamp.desc()).all()

    return render_template('student/student_list_not_current.html', students=students)


@student.route('/<student_id>', methods=['GET', 'POST'])
@roles_required('admin')
def info(student_id):
    current_student = Student.query.filter_by(id=student_id).first()
    if current_student:
        return render_template('student/student_info.html', student=current_student)
    else:
        flash(_('Student did not find'), 'danger')
        return redirect(url_for('student.student_list'))


@student.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    current_schools = School.query.filter_by(current=True).order_by(School.name.asc()).all()
    # Now forming the list of tuples for SelectField
    school_list = [(i.id, i.name) for i in current_schools]

    form = StudentForm()
    form.default_school_id.choices = [(0, "---")]+school_list
    if form.validate_on_submit():
        new_student = Student()
        form.dob.data = datetime.strptime('{}/{}/{}'.format(form.dob_month.data, form.dob_day.data, form.dob_year.data),
                                          '%m/%d/%Y')
        form.populate_obj(new_student)
        current_user.students.append(new_student)
        db.session.commit()
        flash(_('Student has been created'), 'success')
        return redirect(url_for('student.enroll_student', student_id=new_student.id))

    if form.errors:
        for error in form.errors.values():
            flash(error, 'danger')

    return render_template('student/add.html', form=form, step=2)  # step=2 for progressbar


@student.route('/<student_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    current_student = Student.query.filter_by(id=student_id).first()
    if not current_student or (current_student not in current_user.students and not current_user.has_role(
            'admin')):  # TODO or current_student not in current_user.students
        current_app.logger.warning(
            'User is trying to edit not his student. user_id = {} student_id = {}'.format(current_user.id, student_id))
        flash(_('Student does not find'), 'danger')
        return redirect(url_for('user.main'))
    current_schools = School.query.filter_by(current=True).order_by(School.name.asc()).all()
    # Now forming the list of tuples for SelectField
    school_list = [(i.id, i.name) for i in current_schools]
    form = StudentForm(obj=current_student)
    form.default_school_id.choices = [(0, "---")] + school_list

    if form.validate_on_submit():
        form.dob.data = datetime.strptime('{}/{}/{}'.format(form.dob_month.data, form.dob_day.data, form.dob_year.data),
                                          '%m/%d/%Y')
        form.populate_obj(current_student)
        # save to db
        db.session.commit()
        flash(_('Student has been updated'), 'success')
        return redirect(url_for('user.main'))

    form.dob_month.data = form.dob.data.strftime("%m")
    form.dob_day.data = form.dob.data.strftime("%d")
    form.dob_year.data = form.dob.data.strftime("%Y")


    return render_template('student/edit.html', form=form, student_id=student_id)


@student.route('/<student_id>/enroll', methods=['GET', 'POST'])
@login_required
def enroll_student(student_id):
    # list all classes available for current_student
    current_student = Student.query.filter_by(id=student_id).first()
    if not current_student or (current_student not in current_user.students and not current_user.has_role('admin')):
        current_app.logger.warning(
            'User is trying to enroll not his student. user_id = {} student_id = {}'.format(current_user.id,
                                                                                            student_id))
        flash(_('Student does not find'), 'danger')
        return redirect(url_for('user.main'))
    current_school = School.query.filter_by(id=current_student.default_school_id).first()
    current_classes = current_school.classes.filter_by(current=True).order_by(Schdl_Class.day_of_week.asc(), Schdl_Class.class_time_start.asc()).all()
    enrolled_classes = Schdl_Class.query.filter(and_(Schdl_Class.enrollments.any(student_id=current_student.id),
                                                     Schdl_Class.enrollments.any(current=True))).all()

    return render_template('student/enroll.html', current_classes=current_classes, student=current_student,
                           current_school=current_school, enrolled_classes=enrolled_classes,
                           step=3)  # step=3 for progressbar
