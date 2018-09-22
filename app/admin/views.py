from flask import render_template, Blueprint, current_app, redirect, url_for, flash
from flask_security import current_user, roles_required

from app import db
from app.admin.forms import UserForm
from app.models import Teacher, Subject, Schdl_Class, Event, User, Student

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def main():
    current_app.logger.info("Admin {} has been signed in to admin console".format(current_user.email))
    return render_template('admin/dashboard.html')


@admin.route('/teacher', methods=['GET', 'POST'])
@roles_required('admin')
def teacher_list():
    teachers = Teacher.query.filter_by(current=True).all()
    return render_template('admin/teacher_list.html', teachers=teachers, current_steachers_only=True)


@admin.route('/subject', methods=['GET', 'POST'])
@roles_required('admin')
def subject_list():
    subjects = Subject.query.filter_by(current=True).all()
    return render_template('admin/subject_list.html', subjects=subjects)


@admin.route('/class', methods=['GET', 'POST'])
@roles_required('admin')
def class_list():
    classes = Schdl_Class.query.filter_by(current=True).all()
    return render_template('admin/class_list.html', classes=classes, current_classes_only=True)


@admin.route('/event', methods=['GET', 'POST'])
@roles_required('admin')
def event_list():
    events = Event.query.filter_by().all()
    # TODO current_events_only - by date or Schdl_Class.current = True. if today in range(start_date_of_class, end_date_of_class)
    return render_template('admin/event_list.html', events=events, current_events_only=False)


@admin.route('/user/<user_id>/edit', methods=['GET', 'POST'])
@roles_required('admin')
def user_edit(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = UserForm()

    if form.validate_on_submit():
        form.populate_obj(user)
        # save to db
        db.session.commit()
        flash(user.first_name + " " + user.last_name + " edited", "success")
        return redirect(url_for('admin.user_list'))
    else:
        if user:
            form = UserForm(obj=user)
            return render_template('admin/user_edit.html', form=form, user_id=user_id)
        else:
            flash("User with id " + str(user_id) + " did not find", "danger")
            return redirect(url_for('admin.user_list'))


@admin.route('/students', methods=['GET', 'POST'])
@roles_required('admin')
def student_list():
    students = Student.query.all()
    return render_template('admin/student_list.html', students=students)
