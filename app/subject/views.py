from flask import render_template, Blueprint, flash, redirect, url_for
from flask_babel import _
from flask_security import roles_required

from app import db
from app.models import Subject
from .forms import SubjectForm

subject = Blueprint('subject', __name__, template_folder='templates')


@subject.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def subject_list():
    subjects = Subject.query.all()
    return render_template('subject/subject_list.html', subjects=subjects)


@subject.route('/<subject_id>', methods=['GET', 'POST'])
@roles_required('admin')
def info(subject_id):
    current_subject = Subject.query.filter_by(id=subject_id).first()
    if current_subject:
        return render_template('subject/subject_info.html', subject=current_subject)
    else:
        flash(_('(Subject did not find'), 'danger')
        return redirect(url_for('subject.subject_list'))


@subject.route('/add', methods=['GET', 'POST'])
@roles_required('admin')
def add_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        new_subject = Subject()
        form.populate_obj(new_subject)
        # save new school to db
        db.session.add(new_subject)
        db.session.commit()
        flash(_('Subject has been created'), 'success')
        return redirect(url_for('subject.subject_list'))
    else:
        return render_template('subject/add.html', form=form)


@subject.route('/<subject_id>/edit', methods=['GET', 'POST'])
@roles_required('admin')
def edit_subject(subject_id):
    current_subject = Subject.query.filter_by(id=subject_id).first()
    form = SubjectForm()
    if form.validate_on_submit():
        form.populate_obj(current_subject)
        #save to db
        db.session.commit()
        flash(_('Subject has been updated'), 'success')
        return redirect(url_for('subject.subject_list'))
    else:
        if current_subject:
            form = SubjectForm(obj=current_subject)
            return render_template('subject/edit.html', form=form, subject_id=subject_id)
        else:
            flash(_('Subject did not find'), 'danger')
            return redirect(url_for('subject.subject_list'))
