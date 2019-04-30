from flask import render_template, Blueprint, flash, redirect, url_for, abort, request
from flask_babelex import _
from flask_security import roles_required, roles_accepted, current_user

from app import db
from app.models import Student, Award, Subject, StudentAwards, Schdl_Class
from .forms import AwardForm, StudentAwardForm, AwardEditForm, StudentEditAwardForm

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


@award.route('/export', methods=['GET', 'POST'])
@roles_required('admin')
def export():
    award_records = StudentAwards.query.all()
    ma_subject = Subject.query.filter_by(id=7).first()
    html = []
    for ma_class in ma_subject.classes:
        for enrollment in ma_class.enrollments:
            if enrollment.current:
                for award_record in enrollment.student.awards:
                    html.append({"student_name": enrollment.student.first_name + " " + enrollment.student.last_name,
                                 "date": award_record.date.isoformat(), "note": award_record.note,
                                 "school": enrollment.schdl_class.school.name, "class": enrollment.schdl_class.subject.name,
                                 "time": enrollment.schdl_class.class_time_start.isoformat(), "belt": award_record.award.name})
    import json
    html = json.dumps(html)
    return str(html)


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


@award.route('/student/<student_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def student_add(student_id):
    # Add Award record to Student
    form = StudentAwardForm()
    awards = Award.query.order_by(Award.subject_id.asc(), Award.rank.asc()).all()

    award_list = [(i.id, i.subject.name + ' - ' + i.name) for i in awards]
    form.award_id.choices = award_list
    if form.validate_on_submit():
        current_student = Student.query.filter_by(id=student_id).first()
        new_award_record = StudentAwards()
        form.populate_obj(new_award_record)
        db.session.add(new_award_record)
        db.session.commit()
        flash(_('Award has been added '), 'success')
        return redirect(url_for('student.info', student_id=current_student.id))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(err)
        form.student_id.data = student_id
        return render_template('award/modal_add_for_student.html', form=form)


@award.route('/add_record/<student_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def add_record(student_id):
    name = request.form['name']
    award_id = request.form['value']
    student_id = request.form['pk']
    # note = request.form['note']

    if student_id:
        current_student = Student.query.filter_by(id=student_id).first()
        if current_student:
            new_award_record = StudentAwards(student_id=current_student.id, award_id=award_id)  # note=note)
            db.session.add(new_award_record)
            db.session.commit()
        return render_template('page.html'), 200
    else:
        return render_template('page.html'), 404



@award.route('/class/<class_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'teacher')
def add_to_class(class_id):
    # Add Award records to Class
    current_class = Schdl_Class.query.filter_by(id=class_id).first()

    # Check if current user has access to class
    access_to_class = False
    if current_user.has_role('admin'):
        access_to_class = True
    elif current_user.has_role('teacher'):
        for teacher in current_user.teachers:
            if current_class in teacher.classes:
                access_to_class = True

    if not current_class or not access_to_class:
        flash(_('Class did not find'), 'danger')
        abort(404)

    awards = Award.query.filter_by(subject_id=current_class.subject.id).order_by(Award.rank.asc()).all()

    award_list = [{"value": i.id, "text": i.subject.name + " - " + i.name} for i in awards]
    return render_template('award/class.html', current_class=current_class, award_list=award_list)


@award.route('/awardrecord/<award_record_id>/edit', methods=['GET', 'POST'])
@roles_accepted('admin')
def student_edit(award_record_id):
    # Edit Award record of Student
    award_record = StudentAwards.query.filter_by(id=award_record_id).first()
    if award_record:
        form = StudentEditAwardForm(obj=award_record)

        awards = Award.query.order_by(Award.subject_id.asc(), Award.rank.asc()).all()

        award_list = [(i.id, i.subject.name + ' - ' + i.name) for i in awards]
        form.award_id.choices = award_list

        if form.validate_on_submit():
            form.populate_obj(award_record)
            db.session.commit()
            flash(_('Award record has been updated'), 'success')
            return redirect(url_for('student.info', student_id=award_record.student_id))
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    print(err)
            return render_template('award/modal_edit_for_student.html', form=form)


@award.route('/awardrecord/<award_record_id>/delete', methods=['GET', 'POST'])
@roles_accepted('admin')
def student_delete(award_record_id):
    # Delete Award record of Student
    award_record = StudentAwards.query.filter_by(id=award_record_id).first()
    student_id = award_record.student_id
    if award_record:
        if award:
            db.session.delete(award_record)
            db.session.commit()
            flash(_('Award record has been deleted'), 'success')
    return redirect(url_for('student.info', student_id=student_id))
