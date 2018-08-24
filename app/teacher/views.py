from flask import Flask, request, render_template, session, Blueprint, flash, redirect, url_for
from app import db
from .models import Teacher
from .forms import TeacherForm


teacher = Blueprint('teacher', __name__, template_folder='templates')


@teacher.route('/', methods=['GET', 'POST'])
def main():
    teachers = Teacher.query.filter_by(current=True).all()
    return render_template('teacher/teacher_list.html', teachers=teachers, current_teachers_only=True)


@teacher.route('/all', methods=['GET', 'POST'])
def teacher_list():
    teachers = Teacher.query.all()
    return render_template('teacher/teacher_list.html', teachers=teachers, current_teachers_only=False)


@teacher.route('/<teacher_id>', methods=['GET', 'POST'])
def info(teacher_id):
    current_teacher = Teacher.query.filter_by(id=teacher_id).first()
    if current_teacher:
        return render_template('teacher/teacher_info.html', teacher=current_teacher)
    else:
        flash("Teacher with id " + str(teacher_id) + " did not find", "danger")
        return redirect(url_for('teacher.main'))



@teacher.route('/add', methods=['GET', 'POST'])
def add_teacher():
    form = TeacherForm()
    if form.validate_on_submit():
        new_teacher = Teacher()
        form.populate_obj(new_teacher)
        # save new school to db
        db.session.add(new_teacher)
        db.session.commit()
        flash(new_teacher.first_name + " " + new_teacher.last_name + " created", "success")
        return redirect(url_for('teacher.main'))
    else:
        return render_template('teacher/add.html', form=form)



@teacher.route('/edit/<teacher_id>', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    current_teacher = Teacher.query.filter_by(id=teacher_id).first()
    form = TeacherForm()
    if form.validate_on_submit():
        form.populate_obj(current_teacher)
        #save to db
        db.session.commit()
        flash(current_teacher.first_name + " " + current_teacher.last_name + " edited", "success")
        return redirect(url_for('teacher.main'))
    else:
        if current_teacher:
            form = TeacherForm(obj=current_teacher)
            return render_template('teacher/edit.html', form=form, teacher_id=teacher_id)
        else:
            flash("Teacher with id " + str(teacher_id) + " did not find", "danger")
            return redirect(url_for('teacher.main'))
