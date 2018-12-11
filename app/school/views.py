from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_babelex import _
from flask_security import roles_required

from app import db
from app.models import School
from app.school.forms import SchoolForm

school = Blueprint('school', __name__, template_folder='templates')


@school.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def school_list():
    if request.method == 'POST':
        # TODO csrf_token to ajax request
        data = request.form['action']
        print(data)
        data = request.form.getlist('schools')
        for school_id in data:
            school = School.query.filter_by(id=school_id).first()
            print(school.name)
    schools = School.query.filter_by(current=True).all()
    return render_template('school/list.html', schools=schools, current_schools_only=True)


@school.route('/all', methods=['GET', 'POST'])
@roles_required('admin')
def school_all_list():
    schools = School.query.filter_by().all()
    return render_template('school/list.html', schools=schools, current_schools_only=False)


@school.route('/add', methods=['GET', 'POST'])
@roles_required('admin')
def school_add():
    form = SchoolForm()
    if form.validate_on_submit():
        new_school = School()
        form.populate_obj(new_school)
        # save new school to db
        db.session.add(new_school)
        db.session.commit()
        flash(_('School has been created'), 'success')
        return redirect(url_for('school.school_list'))
    else:
        return render_template('school/add_edit.html', form=form, action='add')


@school.route('/<school_id>', methods=['GET', 'POST'])
@roles_required('admin')
def school_info(school_id):
    current_school = School.query.filter_by(id=school_id).first()
    if current_school:
        return render_template('school/info.html', school=current_school)
    else:
        flash(_('School did not find'), 'danger')
        return redirect(url_for('school.school_list'))


@school.route('/<school_id>/edit', methods=['GET', 'POST'])
@roles_required('admin')
def school_edit(school_id):
    current_school = School.query.filter_by(id=school_id).first()
    form = SchoolForm()
    if form.validate_on_submit():
        form.populate_obj(current_school)
        # save to db
        db.session.commit()
        flash(_('School has been updated'), 'success')
        return redirect(url_for('school.school_list'))
    else:
        if current_school:
            form = SchoolForm(obj=current_school)
            return render_template('school/add_edit.html', form=form, action='edit', school=current_school)
        else:
            flash(_('School did not find'), 'danger')
            return redirect(url_for('school.school_list'))
