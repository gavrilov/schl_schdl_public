from flask import render_template, Blueprint, flash, redirect, url_for, request, abort, jsonify
from flask_babelex import _
from flask_security import roles_required, current_user
from datetime import datetime
import re

from app import db
from app.dashboard.forms import AddContactForm, TeacherToClassForm, EditContactForm
from app.student.forms import StudentForm
from app.models import User, Student, Teacher, Enrollment, School, UserContacts, Schdl_Class


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


@dashboard.route('/school', methods=['GET', 'POST'])
@roles_required('school')
def school_dashboard():
    # Dashboard for teachers
    return render_template('dashboard/dashboard_school.html')


@dashboard.route('/add_contact_information', methods=['GET', 'POST'])
@roles_required('admin')
def add_contact_information():
    user_id = request.args.get('user_id')
    # user_id = request.form['user_id']
    form = AddContactForm()
    if form.validate_on_submit():
        contact_info = UserContacts()
        form.populate_obj(contact_info)
        if contact_info.phone:
            contact_info.phone = re.sub("\D", "", contact_info.phone)
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


@dashboard.route('/edit_contact_information/<contact_id>', methods=['GET', 'POST'])
@roles_required('admin')
def edit_contact_information(contact_id):
    contact_info = UserContacts.query.filter_by(id=contact_id).first()
    if contact_info:
        form = EditContactForm(obj=contact_info)
    else:
        flash(_('Contact information did not find'), 'success')
    # user_id = request.form['user_id']
    if form.validate_on_submit():
        form.populate_obj(contact_info)
        if contact_info.phone:
            contact_info.phone = re.sub("\D", "", contact_info.phone)
        db.session.commit()
        flash(_('Contact information has been updated'), 'success')
        return redirect(url_for('user.user_info', user_id=contact_info.user_id))

    if form.errors:
        print(form.errors)
        for error in form.errors.values():
            flash(error, 'danger')

    return render_template('dashboard/edit_contact_info.html', form=form, contact_id=contact_id)



@dashboard.route('/delete_contact_information/<contact_id>', methods=['GET', 'POST'])
@roles_required('admin')
def delete_contact_information(contact_id):
    contact_info = UserContacts.query.filter_by(id=contact_id).first()
    user_id = contact_info.user_id
    if not contact_info:
        flash(_('Contact information did not find'), 'danger')

    db.session.delete(contact_info)
    db.session.commit()
    flash(_('Contact information has been deleted'), 'success')
    return redirect(url_for('user.user_info', user_id=user_id))


@dashboard.route('/teacher_to_class', methods=['POST', 'DELETE'])
@roles_required('admin')
def teacher_to_class():
    teacher_id = request.form['teacher_id']
    class_id = request.form['class_id']

    if not teacher_id or not class_id:
        return abort(404)

    teacher = Teacher.query.filter_by(id=teacher_id).first()
    current_class = Schdl_Class.query.filter_by(id=class_id).first()

    if not teacher or not current_class:
        return abort(404)

    # add current class to list of teacher classes
    if request.method == 'POST':
        if current_class not in teacher.classes:
            teacher.classes.append(current_class)
            db.session.commit()
        else:
            flash(_('Teacher already has access to that class'), 'danger')

    elif request.method == 'DELETE':
        teacher.classes.remove(current_class)
        db.session.commit()
        return render_template('page.html'), 200
    else:
        return abort(404)


    return redirect(url_for('schdl_class.edit_class', class_id=current_class.id))


@dashboard.route('/modal_teacher_to_class/<class_id>', methods=['GET'])
@roles_required('admin')
def modal_teacher_to_class(class_id):
    form = TeacherToClassForm()
    # class_id = request.form['class_id']
    teachers = Teacher.query.filter_by(current=True).all()
    teacher_list = [(i.id, i.user.first_name + ' ' + i.user.last_name) for i in teachers]
    form.teacher_id.choices = teacher_list
    form.class_id.data = class_id
    return render_template('dashboard/modal_teacher_to_class.html', form=form)


@dashboard.route('user/<user_id>/student/add/', methods=['GET', 'POST'])
@roles_required('admin')
def add_student(user_id):
    current_schools = School.query.filter_by(current=True).order_by(School.name.asc()).all()
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
