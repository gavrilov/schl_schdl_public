from flask import Flask, request, render_template, session, Blueprint, flash, redirect, url_for
from app import db
from .models import School
from .forms import SchoolForm


school = Blueprint('school', __name__, template_folder='templates')


@school.route('/', methods=['GET', 'POST'])
def main():
    schools = School.query.filter_by(current=True).all()
    return render_template('school/school_list.html', schools=schools, current_schools_only=True)


@school.route('/all', methods=['GET', 'POST'])
def school_list():
    schools = School.query.all()
    return render_template('school/school_list.html', schools=schools, current_schools_only=False)


@school.route('/<schl_id>', methods=['GET', 'POST'])
def info(schl_id):
    current_school = School.query.filter_by(id=schl_id).first()
    if current_school:
        return render_template('school/school_info.html', school=current_school)
    else:
        flash("School with id " + str(schl_id) + " did not find", "danger")
        return redirect(url_for('school.main'))



@school.route('/add', methods=['GET', 'POST'])
def add_schl():
    form = SchoolForm()
    if form.validate_on_submit():
        new_school = School()
        form.populate_obj(new_school)
        # save new school to db
        db.session.add(new_school)
        db.session.commit()
        flash(new_school.school_name + " created", "success")
        return redirect(url_for('school.main'))
    else:
        return render_template('school/add.html', form=form)



@school.route('/edit/<schl_id>', methods=['GET', 'POST'])
def edit_schl(schl_id):
    current_school = School.query.filter_by(id=schl_id).first()
    form = SchoolForm()
    if form.validate_on_submit():
        form.populate_obj(current_school)
        #save to db
        db.session.commit()
        flash(current_school.school_name + " edited", "success")
        return redirect(url_for('school.main'))
    else:
        if current_school:
            form = SchoolForm(obj=current_school)
            return render_template('school/edit.html', form=form, schl_id=schl_id)
        else:
            flash("School with id " + str(schl_id) + " did not find", "danger")
            return redirect(url_for('school.main'))
