from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_babelex import _
from flask_security import roles_required, current_user
from datetime import datetime

from app import db
from app.dashboard.forms import AddContactForm
from app.student.forms import StudentForm
from app.models import User, Student, Teacher, Enrollment, School, UserContacts


dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def main():
    # Dashboard for Admins
    users = User.query.count()
    users_without_students = User.query.filter(~User.students.any()).count()
    teachers = Teacher.query.count()
    users_without_students -= teachers  # dont count teachers
    students = Student.query.count()
    not_enrolled_students = Student.query.filter(~Student.enrollments.any()).count()
    enrollments_num = Enrollment.query.count()
    five_last_enrollments = Enrollment.query.order_by(Enrollment.id.desc()).limit(5).all()
    return render_template('dashboard/dashboard.html', users=users, teachers=teachers, students=students, enrollments_num=enrollments_num,
                           five_last_enrollments=five_last_enrollments, users_without_students=users_without_students,
                           not_enrolled_students=not_enrolled_students)


@dashboard.route('/teacher', methods=['GET', 'POST'])
@roles_required('teacher')
def teacher_dashboard():
    # Dashboard for teachers
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher or not teacher.current:
        flash(_('Teacher did not find. Please contact administration'), 'danger')
        return redirect(url_for('hello_world'))
    return render_template('dashboard/dashboard_teacher.html', teacher=teacher)


@dashboard.route('/add_contact_information', methods=['GET', 'POST'])
@roles_required('admin')
def add_contact_information():
    user_id = request.args.get('user_id')
    # user_id = request.form['user_id']
    form = AddContactForm()
    if form.validate_on_submit():
        contact_info = UserContacts()
        form.populate_obj(contact_info)

        contact_info.user_id = user_id
        db.session.add(contact_info)
        db.session.commit()
        flash(_('Contact information has been updated'), 'success')
        return redirect(url_for('user.user_info', user_id=user_id))

    if form.errors:
        print(form.errors)
        for error in form.errors.values():
            flash(error, 'danger')

    return render_template('dashboard/add_contact_info.html', form=form, user_id=user_id)  # step=1 for progress bar



@dashboard.route('user/<user_id>/student/add/', methods=['GET', 'POST'])
@roles_required('admin')
def add_student(user_id):
    current_schools = School.query.filter_by(current=True, hide_from_users=False).order_by(School.name.asc()).all()
    # Now forming the list of tuples for SelectField
    school_list = [(i.id, i.name) for i in current_schools]
    this_user = User.query.filter_by(id=user_id).first()
    if not this_user:
        flash(_('User did not find'), 'danger')
        return redirect(url_for('user.user_list'))

    form = StudentForm()
    form.default_school_id.choices = [(0, "---")]+school_list
    if form.validate_on_submit():
        new_student = Student()
        form.dob.data = datetime.strptime('{}/{}/{}'.format(form.dob_month.data, form.dob_day.data, form.dob_year.data),
                                          '%m/%d/%Y')
        form.populate_obj(new_student)
        this_user.students.append(new_student)
        db.session.commit()
        flash(_('Student has been created'), 'success')
        return redirect(url_for('student.info', student_id=new_student.id))

    if form.errors:
        for error in form.errors.values():
            flash(error, 'danger')

    return render_template('dashboard/student_add.html', form=form, user=this_user)
