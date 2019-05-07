from flask import render_template, Blueprint, flash, redirect, url_for
from flask_babelex import _
from flask_security import roles_required

from app import db
from app.models import Semester
from .forms import SemesterForm

semester = Blueprint('semester', __name__, template_folder='templates')


@semester.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def semester_list():
    semesters = Semester.query.all()
    return render_template('semester/semester_list.html', semesters=semesters)


@semester.route('/<semester_id>', methods=['GET', 'POST'])
@roles_required('admin')
def info(semester_id):
    current_semester = Semester.query.filter_by(id=semester_id).first()
    if current_semester:
        return render_template('semester/semester_info.html', semester=current_semester)
    else:
        flash(_('Semester did not find'), 'danger')
        return redirect(url_for('semester.semester_list'))


@semester.route('/add', methods=['GET', 'POST'])
@roles_required('admin')
def add_semester():
    form = SemesterForm()
    if form.validate_on_submit():
        new_semester = Semester()
        form.populate_obj(new_semester)
        # save new school to db
        db.session.add(new_semester)
        db.session.commit()
        flash(_('Semester has been created'), 'success')
        return redirect(url_for('semester.semester_list'))
    else:
        return render_template('semester/add.html', form=form)


@semester.route('/<semester_id>/edit', methods=['GET', 'POST'])
@roles_required('admin')
def edit_semester(semester_id):
    current_semester = Semester.query.filter_by(id=semester_id).first()
    form = SemesterForm()
    if form.validate_on_submit():
        form.populate_obj(current_semester)
        # save to db
        db.session.commit()
        flash(_('Semester has been updated'), 'success')
        return redirect(url_for('semester.semester_list'))
    else:
        if current_semester:
            form = SemesterForm(obj=current_semester)
            return render_template('semester/edit.html', form=form, semester_id=semester_id)
        else:
            flash(_('Semester did not find'), 'danger')
            return redirect(url_for('semester.semester_list'))
