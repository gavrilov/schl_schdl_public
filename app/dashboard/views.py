from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_babelex import _
from flask_security import roles_required, current_user

from app import db
from app.dashboard.forms import AddContactForm
from app.models import User, Student, Teacher, Enrollment
from app.models import UserContacts

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
