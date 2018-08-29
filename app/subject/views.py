from flask import Flask, request, render_template, session, Blueprint, flash, redirect, url_for
from app import db
from app.models import Subject
from .forms import SubjectForm


subject = Blueprint('subject', __name__, template_folder='templates')


@subject.route('/', methods=['GET', 'POST'])
def main():
    subjects = Subject.query.all()
    return render_template('subject/subject_list.html', subjects=subjects)


@subject.route('/<subject_id>', methods=['GET', 'POST'])
def info(subject_id):
    current_subject = Subject.query.filter_by(id=subject_id).first()
    if current_subject:
        return render_template('subject/subject_info.html', subject=current_subject)
    else:
        flash("Subject with id " + str(subject_id) + " did not find", "danger")
        return redirect(url_for('subject.main'))



@subject.route('/add', methods=['GET', 'POST'])
def add_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        new_subject = Subject()
        form.populate_obj(new_subject)
        # save new school to db
        db.session.add(new_subject)
        db.session.commit()
        flash(new_subject.name + " created", "success")
        return redirect(url_for('subject.main'))
    else:
        return render_template('subject/add.html', form=form)


@subject.route('/edit/<subject_id>', methods=['GET', 'POST'])
def edit_subject(subject_id):
    current_subject = Subject.query.filter_by(id=subject_id).first()
    form = SubjectForm()
    if form.validate_on_submit():
        form.populate_obj(current_subject)
        #save to db
        db.session.commit()
        flash(current_subject.name + " edited", "success")
        return redirect(url_for('subject.main'))
    else:
        if current_subject:
            form = SubjectForm(obj=current_subject)
            return render_template('subject/edit.html', form=form, subject_id=subject_id)
        else:
            flash("Subject with id " + str(subject_id) + " did not find", "danger")
            return redirect(url_for('subject.main'))
