from flask import render_template, Blueprint, redirect, url_for, flash
from flask_security import roles_required

from app import db
from app.models import Teacher
from .forms import TeacherForm

teacher = Blueprint('teacher', __name__, template_folder='templates')


@teacher.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def teacher_list():
    teachers = Teacher.query.filter_by(current=True).all()
    return render_template('teacher/list.html', teachers=teachers, current_teachers_only=True)


@teacher.route('/all', methods=['GET', 'POST'])
@roles_required('admin')
def teacher_all_list():
    teachers = Teacher.query.all()
    return render_template('teacher/list.html', teachers=teachers, current_teachers_only=False)


@teacher.route('/add', methods=['GET', 'POST'])
@roles_required('admin')
def teacher_add():
    form = TeacherForm()
    if form.validate_on_submit():
        new_teacher = Teacher()
        form.populate_obj(new_teacher)
        # save new school to db
        db.session.add(new_teacher)
        db.session.commit()
        flash("Teacher {} {} created".format(new_teacher.first_name, new_teacher.last_name), "success")
        return redirect(url_for('teacher.teacher_list'))
    else:
        return render_template('teacher/add_edit.html', form=form, action='add')


@teacher.route('/<teacher_id>', methods=['GET', 'POST'])
@roles_required('admin')
def teacher_info(teacher_id):
    current_teacher = Teacher.query.filter_by(id=teacher_id).first()
    if current_teacher:
        return render_template('teacher/info.html', teacher=current_teacher)
    else:
        flash("Teacher with id {} did not find".format(teacher_id), "danger")
        return redirect(url_for('teacher.teacher_list'))


@teacher.route('/<teacher_id>/edit', methods=['GET', 'POST'])
@roles_required('admin')
def teacher_edit(teacher_id):
    current_teacher = Teacher.query.filter_by(id=teacher_id).first()
    form = TeacherForm()
    if form.validate_on_submit():
        form.populate_obj(current_teacher)
        #save to db
        db.session.commit()
        flash("Teacher {} {} edited".format(current_teacher.user.first_name, current_teacher.user.last_name), "success")
        return redirect(url_for('teacher.teacher_list'))
    else:
        if current_teacher:
            form = TeacherForm(obj=current_teacher)
            return render_template('teacher/add_edit.html', form=form, teacher_id=teacher_id)
        else:
            flash("Teacher with id {} did not find".format(teacher_id), "danger")
            return redirect(url_for('teacher.teacher_list'))
