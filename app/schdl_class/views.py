from flask import Flask, request, render_template, session, Blueprint, flash, redirect, url_for
from app import db
from .forms import ClassForm
from app.models import Schdl_Class
from app.models import School
from app.models import Teacher
from app.models import Subject

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
def main():
    classes = Schdl_Class.query.filter_by(current=True).all()
    return render_template('schdl_class/class_list.html', classes=classes, current_classes_only=True)


@schdl_class.route('/all', methods=['GET', 'POST'])
def class_list():
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
    teacher_list = [(i.id, i.first_name) for i in current_teachers]
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
        return redirect(url_for('schdl_class.main'))
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
        teacher_list = [(i.id, i.first_name) for i in current_teachers]
        subject_list = [(i.id, i.name) for i in current_subjects]

        form.school_id.choices = school_list
        form.teacher_id.choices = teacher_list
        form.subject_id.choices = subject_list

        if form.validate_on_submit():
            form.populate_obj(current_class)
            #save to db
            db.session.commit()
            flash(current_class.subject.name + " class edited", "success")
            return redirect(url_for('schdl_class.main'))
        else:
            return render_template('schdl_class/edit.html', form=form, class_id=class_id)
    else:
        flash("Class with id " + str(class_id) + " did not find", "danger")
        return redirect(url_for('schdl_class.main'))
