from flask import render_template, Blueprint, flash, redirect, url_for, current_app
from flask_security import current_user, login_required

from app import db
from app.models import Student, Schdl_Class
from .forms import StudentForm

student = Blueprint('student', __name__, template_folder='templates')


@student.route('/', methods=['GET', 'POST'])
def main():
    # TODO filter current student by current students or so
    students = Student.query.filter_by().all()
    return render_template('student/student_list.html', students=students, current_students_only=False)


@student.route('/all', methods=['GET', 'POST'])
def student_list():
    students = Student.query.all()
    return render_template('student/student_list.html', students=students, current_students_only=False)


@student.route('/<student_id>', methods=['GET', 'POST'])
def info(student_id):
    current_student = Student.query.filter_by(id=student_id).first()
    if current_student:
        return render_template('student/student_info.html', student=current_student)
    else:
        flash("Student with id " + str(student_id) + " did not find", "danger")
        return redirect(url_for('student.main'))


@student.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentForm()

    if form.validate_on_submit():
        new_student = Student()
        form.populate_obj(new_student)
        new_student.user_id = current_user.id
        # save new school to db
        db.session.add(new_student)
        db.session.commit()
        flash(new_student.first_name + " " + new_student.last_name + " created", "success")
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

    form = StudentForm(obj=current_student)

    if form.validate_on_submit():
        print(form.gender.data == 1)
        form.populate_obj(current_student)
        # save to db
        db.session.commit()
        flash(current_student.first_name + " " + current_student.last_name + " edited", "success")
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
    current_classes = Schdl_Class.query.filter_by(current=True).all()
    form = StudentForm(obj=current_student)

    if form.validate_on_submit():
        print(form.gender.data == 1)
        form.populate_obj(current_student)
        # save to db
        db.session.commit()
        flash(current_student.first_name + " " + current_student.last_name + " edited", "success")
        return redirect(url_for('user.main'))

    return render_template('student/enroll.html', current_classes=current_classes, student=current_student)
