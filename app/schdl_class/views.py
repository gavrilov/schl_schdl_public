from flask import render_template, Blueprint, flash, redirect, url_for, current_app
from flask_security import current_user, login_required

from app import db
from app.models import Schdl_Class, Student, Enrollment
from app.models import School
from app.models import Subject
from app.models import Teacher
from .forms import ClassForm

schdl_class = Blueprint('schdl_class', __name__, template_folder='templates')


@schdl_class.route('popup', methods=['GET', 'POST'])
def generate_popup_url():
    # We need it to generate a base of dynamic url for popups
    return False


@schdl_class.route('popup/<class_id>/', methods=['GET', 'POST'])
def generate_popup_html(class_id):
    print('I GOT IT!', class_id)
    form = ClassForm()
    form.title.data = class_id
    return render_template('schdl_class/edit.html', form=form)


@schdl_class.route('/', methods=['GET', 'POST'])
def class_list():
    classes = Schdl_Class.query.filter_by(current=True).all()
    return render_template('schdl_class/class_list.html', classes=classes, current_classes_only=True)


@schdl_class.route('/all', methods=['GET', 'POST'])
def class_all_list():
    classes = Schdl_Class.query.filter_by().all()
    return render_template('schdl_class/class_list.html', classes=classes, current_classes_only=False)


@schdl_class.route('/add', methods=['GET', 'POST'])
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
        flash(new_class.subject.name + " created", "success")
        return redirect(url_for('schdl_class.class_list'))
    else:
        return render_template('schdl_class/add.html', form=form)


@schdl_class.route('/edit/<class_id>', methods=['GET', 'POST'])
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
            flash(current_class.subject.name + " class edited", "success")
            return redirect(url_for('schdl_class.class_list'))
        else:
            return render_template('schdl_class/edit.html', form=form, class_id=class_id)
    else:
        flash("Class with id " + str(class_id) + " did not find", "danger")
        return redirect(url_for('schdl_class.class_list'))


@schdl_class.route('/enroll/<class_id>/<student_id>', methods=['GET', 'POST'])
@login_required
def enroll_class(class_id, student_id):
    current_class = Schdl_Class.query.filter_by(id=class_id).first()
    current_student = Student.query.filter_by(id=student_id).first()

    if not current_class:
        current_app.logger.warning(
            'User is trying to enroll not existing class. user_id = {} class_id = {}'.format(current_user.id,
                                                                                             class_id))
        flash('Class does not find', 'danger')
        return redirect(url_for('user.class_list'))
    if not current_student or current_student.user_id != current_user.id:
        current_app.logger.warning(
            'User is trying to enroll not his student. user_id = {} student_id = {}'.format(current_user.id,
                                                                                            student_id))
        flash("Student does not find", "danger")
        return redirect(url_for('user.class_list'))

    return render_template('schdl_class/enroll.html', current_class=current_class, current_student=current_student)


@schdl_class.route('/payment/<class_id>/<student_id>', methods=['GET', 'POST'])
@login_required
def payment_class(class_id, student_id):
    # TODO get payment with Stripe. If payment successful add Student to enrollments
    current_class = Schdl_Class.query.filter_by(id=class_id).first()
    current_student = Student.query.filter_by(id=student_id).first()

    if not current_class:
        current_app.logger.warning(
            'User is trying to enroll not existing class. user_id = {} class_id = {}'.format(current_user.id,
                                                                                             class_id))
        flash('Class does not find', 'danger')
        return redirect(url_for('user.class_list'))
    if not current_student or current_student.user_id != current_user.id:
        current_app.logger.warning(
            'User is trying to enroll not his student. user_id = {} student_id = {}'.format(current_user.id,
                                                                                            student_id))
        flash("Student does not find", "danger")
        return redirect(url_for('user.class_list'))
    new_enrollment = Enrollment()
    new_enrollment.class_id = current_class.id
    new_enrollment.student_id = current_student.id
    db.session.add(new_enrollment)
    db.session.commit()
    flash("{} has been added to student list of {} classes".format(current_student.first_name,
                                                                   current_class.subject.name), "success")
    return redirect(url_for('user.class_list'))
