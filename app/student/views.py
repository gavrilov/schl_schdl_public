from datetime import datetime

from flask import render_template, Blueprint, flash, redirect, url_for, current_app
from flask_security import current_user, login_required, roles_required

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
    # show students who are not enrolled in any classes
    q = db.session.query(Student)
    students = q.filter(~Student.classes.any()) # ~ means not
    return render_template('student/student_list_not_current.html', students=students)


@student.route('/<student_id>', methods=['GET', 'POST'])
@roles_required('admin')
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
    form.default_school_id.choices = [(0, "---")]+school_list
    if form.validate_on_submit():
        new_student = Student()
        form.dob.data = datetime.strptime('{}/{}/{}'.format(form.dob_month.data, form.dob_day.data, form.dob_year.data),
                                          '%m/%d/%Y')
        form.populate_obj(new_student)
        new_student.user_id = current_user.id  # TODO current_user.students.append(new_student)
        # save new school to db
        db.session.add(new_student)
        db.session.commit()
        flash("Student {} {} has been created".format(new_student.first_name, new_student.last_name), "success")
        return redirect(url_for('student.enroll_student', student_id=new_student.id))

    if form.errors:
        for error in form.errors.values():
            flash(error, 'danger')

    return render_template('student/add.html', form=form)


@student.route('/<student_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    current_student = Student.query.filter_by(id=student_id).first()
    if not current_student or (current_student not in current_user.students and not current_user.has_role(
            'admin')):  # TODO or current_student not in current_user.students
        current_app.logger.warning(
            'User is trying to edit not his student. user_id = {} student_id = {}'.format(current_user.id, student_id))
        flash("Student does not find", "danger")
        return redirect(url_for('user.main'))
    current_schools = School.query.filter_by(current=True).all()
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
        flash("Student {} {} has been updated".format(current_student.first_name, current_student.last_name), "success")
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
        flash("Student does not find", "danger")
        return redirect(url_for('user.main'))
    current_school = School.query.filter_by(id=current_student.default_school_id).first()
    current_classes = current_school.classes.filter_by(current=True).all()
    form = StudentForm(obj=current_student)

    if form.validate_on_submit():
        form.populate_obj(current_student)
        # save to db
        db.session.commit()
        flash("Student {} {} edited".format(current_student.first_name, current_student.last_name), "success")
        return redirect(url_for('user.main'))

    return render_template('student/enroll.html', current_classes=current_classes, student=current_student, current_school=current_school)
