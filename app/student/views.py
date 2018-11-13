from flask import render_template, Blueprint, flash, redirect, url_for, current_app
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
    return render_template('student/student_list.html', students_html=students_html, current_students_only=False)


@student.route('/all', methods=['GET', 'POST'])
def student_all_list():
    students = Student.query.all()
    return render_template('student/student_list.html', students=students, current_students_only=False)


@student.route('/<student_id>', methods=['GET', 'POST'])
def info(student_id):
    current_student = Student.query.filter_by(id=student_id).first()
    if current_student:
        return render_template('student/student_info.html', student=current_student)
    else:
        flash("Student with id {} did not find".format(student_id), "danger")
        return redirect(url_for('student.student_list'))


@student.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    current_schools = School.query.filter_by(current=True).all()
    # Now forming the list of tuples for SelectField
    school_list = [(i.id, i.name) for i in current_schools]

    form = StudentForm()
    form.default_school_id.choices = school_list
    if form.validate_on_submit():
        new_student = Student()
        form.populate_obj(new_student)
        new_student.user_id = current_user.id
        # save new school to db
        db.session.add(new_student)
        db.session.commit()
        flash("Student {} {} created".format(new_student.first_name, new_student.last_name), "success")
        return redirect(url_for('user.main'))

    if form.errors:
        print(form.errors)
        for error in form.errors.values():
            flash(error, 'danger')

    return render_template('student/add.html', form=form)


@student.route('/edit/<student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    current_student = Student.query.filter_by(id=student_id).first()
    if not current_student or current_student.user_id != current_user.id:
        current_app.logger.warning(
            'User is trying to edit not his student. user_id = {} student_id = {}'.format(current_user.id, student_id))
        flash("Student does not find", "danger")
        return redirect(url_for('user.main'))
    current_schools = School.query.filter_by(current=True).all()
    # Now forming the list of tuples for SelectField
    school_list = [(i.id, i.name) for i in current_schools]
    form = StudentForm(obj=current_student)
    form.default_school_id.choices = school_list
    if form.validate_on_submit():
        print(form.gender.data == 1)
        form.populate_obj(current_student)
        # save to db
        db.session.commit()
        flash("Student {} {} has been updated".format(current_student.first_name, current_student.last_name), "success")
        return redirect(url_for('user.main'))

    return render_template('student/edit.html', form=form, student_id=student_id)


@student.route('/enroll/<student_id>', methods=['GET', 'POST'])
@login_required
def enroll_student(student_id):
    current_student = Student.query.filter_by(id=student_id).first()
    if not current_student or current_student.user_id != current_user.id:
        current_app.logger.warning(
            'User is trying to enroll not his student. user_id = {} student_id = {}'.format(current_user.id,
                                                                                            student_id))
        flash("Student does not find", "danger")
        return redirect(url_for('user.main'))
    current_classes = Schdl_Class.query.filter(
        and_(Schdl_Class.current == True, Schdl_Class.school_id == current_student.default_school_id)).all()
    # current_classes = Schdl_Class.query.filter_by(current=True, school.id=current_student.default_school_id).all()
    form = StudentForm(obj=current_student)

    if form.validate_on_submit():
        print(form.gender.data == 1)
        form.populate_obj(current_student)
        # save to db
        db.session.commit()
        flash("Student {} {} edited".format(current_student.first_name, current_student.last_name), "success")
        return redirect(url_for('user.main'))

    return render_template('student/enroll.html', current_classes=current_classes, student=current_student)
