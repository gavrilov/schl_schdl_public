from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_babelex import _
from flask_security import roles_required, current_user, roles_accepted
from .forms import AwardForm, StudentAwardForm, AwardEditForm
from app.models import User, Student, Teacher, Enrollment, Schdl_Class, School, Award, Subject
from app import db

award = Blueprint('award', __name__, template_folder='templates')


@award.route('/', methods=['GET'])
@roles_required('admin')
def list_all():
    # Dashboard for teachers
    awards = Award.query.all()
    return render_template('award/award_list.html', awards=awards)


@award.route('/add', methods=['GET', 'POST'])
@roles_required('admin')
def add():
    form = AwardForm()
    subjects = Subject.query.all()
    subjects_list = [(i.id, i.name) for i in subjects]
    form.subject_id.choices = subjects_list

    if form.validate_on_submit():
        new_award = Award()
        form.populate_obj(new_award)
        db.session.add(new_award)
        db.session.commit()
        return redirect(url_for('award.list_all'))
    return render_template('award/add.html', form=form)


@award.route('/edit/<award_id>', methods=['GET', 'POST'])
@roles_required('admin')
def edit(award_id):
    award = Award.query.filter_by(id=award_id).first()

    if award:
        form = AwardEditForm(obj=award)
        subjects = Subject.query.all()
        subjects_list = [(i.id, i.name) for i in subjects]
        form.subject_id.choices = subjects_list

        if form.validate_on_submit():
            form.populate_obj(award)
            db.session.commit()
            return redirect(url_for('award.list_all'))
        return render_template('award/edit.html', form=form)
    return 'Ok'


@award.route('/add/<award_id>', methods=['GET', 'POST'])
@roles_required('admin')
def delete(award_id):
    award = Award.query.filter_by(id=award_id).first()
    if award:
        db.session.delete(award)
        db.session.commit()
    return redirect(url_for('award.list_all'))


@award.route('/student', methods=['POST'])
@roles_accepted('admin', 'teacher')
def student():
    student_id = request.form['student_id']
    form = StudentAwardForm()
    awards = Award.query.order_by(Award.rank.asc()).all()

    award_list = [(i.id, i.name + '@' + i.subject.name) for i in awards]
    form.award_id.choices = award_list

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


@award.route('/edit/<enrollment_id>', methods=['GET', 'POST'])
@roles_required('admin')
def edit_student(enrollment_id):

    current_classes = Schdl_Class.query.filter_by(current=True).join(School, Schdl_Class.school).order_by(School.name.asc()).all()
    current_enrollment = Enrollment.query.filter_by(id=enrollment_id).first()
    form = StudentAwardForm(obj=current_enrollment)
    class_list = [(i.id, i.school.name + '@' + i.subject.name + ' ' + i.day_of_week + ' ' + (i.class_time_start.strftime("%I:%M %p") if i.class_time_start else "")) for i in current_classes]
    form.class_id.choices = class_list
    if form.validate_on_submit():
        form.populate_obj(current_enrollment)
        db.session.commit()
        flash(_('Enrollment has been updated'), 'success')
        return redirect(url_for('student.info', student_id=current_enrollment.student_id))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(err)
        return render_template('enrollment/modal_edit_enrolment.html', form=form)

