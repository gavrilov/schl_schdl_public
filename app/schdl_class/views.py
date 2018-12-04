from flask import render_template, Blueprint, flash, redirect, url_for, current_app
from flask_security import current_user, login_required, roles_required, roles_accepted
from sqlalchemy import and_

from app import db
from app.models import Schdl_Class, Student, Enrollment, School, Subject, Teacher
from app.payment import charge_customer
from .forms import ClassForm

schdl_class = Blueprint('schdl_class', __name__, template_folder='templates')


@schdl_class.route('/popup', methods=['GET', 'POST'])
def generate_popup_url():
    # We need it to generate a base of dynamic url for popups
    return False


@schdl_class.route('/popup/<class_id>/', methods=['GET', 'POST'])
def generate_popup_html(class_id):
    print('I GOT IT!', class_id)
    form = ClassForm()
    form.title.data = class_id
    return render_template('schdl_class/edit.html', form=form)


@schdl_class.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def class_list():
    classes = Schdl_Class.query.filter_by(current=True).all()
    return render_template('schdl_class/class_list.html', classes=classes, current_classes_only=True)


@schdl_class.route('/all', methods=['GET', 'POST'])
@roles_required('admin')
def class_all_list():
    classes = Schdl_Class.query.filter_by().all()
    return render_template('schdl_class/class_list.html', classes=classes, current_classes_only=False)


@schdl_class.route('/add', methods=['GET', 'POST'])
@roles_required('admin')
def add_class():
    current_schools = School.query.filter_by(current=True).all()
    current_teachers = Teacher.query.filter_by(current=True).all()
    current_subjects = Subject.query.filter_by(current=True).all()
    form = ClassForm()

    # Now forming the list of tuples for SelectField
    school_list = [(i.id, i.name) for i in current_schools]
    teacher_list = [(i.id, i.user.first_name + " " + i.user.last_name) for i in current_teachers]
    subject_list = [(i.id, i.name) for i in current_subjects]

    # passing group_list to the form
    form.school_id.choices = school_list
    form.teacher_id.choices = teacher_list
    form.subject_id.choices = subject_list
    if form.validate_on_submit():
        new_class = Schdl_Class()
        form.populate_obj(new_class)
        # save new school to db
        db.session.add(new_class)
        db.session.commit()
        new_class.info = new_class.subject.default_info  # add default description from subject to class
        db.session.commit()
        flash("{} class at {} has been created".format(new_class.subject.name, new_class.school.name), "success")
        return redirect(url_for('schdl_class.edit_class', class_id=new_class.id))
    else:
        return render_template('schdl_class/add.html', form=form)


@schdl_class.route('/<class_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def info_class(class_id):
    current_class = Schdl_Class.query.filter_by(id=class_id).first()
    if not current_class:
        flash('Class with id = {} did not find'.format(class_id), 'danger')
        redirect('schdl_class.class_list')
    return render_template('dashboard/class_info.html', current_class=current_class)


@schdl_class.route('/<class_id>/edit', methods=['GET', 'POST'])
@roles_required('admin')
def edit_class(class_id):
    current_class = Schdl_Class.query.filter_by(id=class_id).first()
    if current_class:
        form = ClassForm(obj=current_class)

        current_schools = School.query.filter_by(current=True).all()
        current_teachers = Teacher.query.filter_by(current=True).all()
        current_subjects = Subject.query.filter_by(current=True).all()

        # Now forming the list of tuples for SelectField
        school_list = [(i.id, i.name) for i in current_schools]
        teacher_list = [(i.id, i.user.first_name + " " + i.user.last_name) for i in current_teachers]
        subject_list = [(i.id, i.name) for i in current_subjects]

        form.school_id.choices = school_list
        form.teacher_id.choices = teacher_list
        form.subject_id.choices = subject_list

        if form.validate_on_submit():
            form.populate_obj(current_class)
            # save to db
            db.session.commit()
            flash("{} class at {} has been updated".format(current_class.subject.name, current_class.school.name),
                  "success")
            return redirect(url_for('schdl_class.class_list'))
        else:
            return render_template('schdl_class/edit.html', form=form, current_class=current_class)
    else:
        flash("Class with id " + str(class_id) + " did not find", "danger")
        return redirect(url_for('schdl_class.class_list'))


@schdl_class.route('/<class_id>/enroll/<student_id>', methods=['GET', 'POST'])
@login_required
def enroll_class(class_id, student_id):
    current_class = Schdl_Class.query.filter_by(id=class_id).first()
    current_student = Student.query.filter_by(id=student_id).first()

    if not current_class:
        current_app.logger.warning(
            'User is trying to enroll not existing class. user_id = {} class_id = {}'.format(current_user.id,
                                                                                             class_id))
        flash('Class does not find', 'danger')
        return redirect(url_for('user.main'))
    if not current_student or (current_student not in current_user.students and not current_user.has_role('admin')):
        current_app.logger.warning(
            'User is trying to enroll not his student. user_id = {} student_id = {}'.format(current_user.id,
                                                                                            student_id))
        flash("Student does not find", "danger")
        return redirect(url_for('user.main'))
    current_enrollment = Enrollment.query.filter(
        and_(Enrollment.student_id == student_id, Enrollment.class_id == class_id, Enrollment.current == True)).first()
    return render_template('schdl_class/enroll.html', current_class=current_class, current_student=current_student,
                           current_enrollment=current_enrollment)


@schdl_class.route('/<class_id>/payment/<student_id>', methods=['GET', 'POST'])
@login_required
def payment_class(class_id, student_id):
    current_class = Schdl_Class.query.filter_by(id=class_id).first()
    current_student = Student.query.filter_by(id=student_id).first()
    current_enrollment = Enrollment.query.filter(
        and_(Enrollment.student_id == student_id, Enrollment.class_id == class_id, Enrollment.current == True)).first()
    if current_enrollment:
        flash('Your child already enrolled, you do not need to pay second time', 'warning')
        return redirect(url_for('user.main'))

    if not current_class:
        current_app.logger.warning(
            'User is trying to enroll not existing class. user_id = {} class_id = {}'.format(current_user.id,
                                                                                             class_id))
        flash('Class does not find', 'danger')
        return redirect(url_for('user.main'))

    if not current_student or current_student not in current_user.students:
        current_app.logger.warning(
            'User is trying to enroll not his student. user_id = {} student_id = {}'.format(current_user.id,
                                                                                            student_id))
        flash("Student does not find", "danger")
        return redirect(url_for('user.main'))
    description = "{} class at {} for {} {}".format(current_class.subject.name, current_class.school.name,
                                                    current_student.first_name, current_student.last_name)
    charge = charge_customer(int(current_class.price * 100), description)
    if charge.status == 'succeeded':
        # TODO improve code how to add new enrollment, make def
        new_enrollment = Enrollment()
        new_enrollment.class_id = current_class.id
        new_enrollment.student_id = current_student.id
        new_enrollment.current = True
        db.session.add(new_enrollment)
        db.session.commit()
        flash("{} has been added to student list of {} classes".format(current_student.first_name,
                                                                       current_class.subject.name), "success")
        return render_template('payment/successful.html', charge=charge, current_class=current_class,
                               current_student=current_student)
    else:
        flash(charge.failure_message, 'danger')
        flash("Something wrong with your payment", "danger")
        return render_template('payment/failed.html', charge=charge)
    # return redirect(url_for('student.enroll_student', student_id=current_student.id))
