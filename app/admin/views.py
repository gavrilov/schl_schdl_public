from flask import render_template, Blueprint, current_app, redirect, url_for, flash, request
from flask_security import current_user, roles_required

from app import db
from app.admin.forms import UserForm, SchoolForm
from app.models import School, Teacher, Subject, Schdl_Class, Event, User, Student

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def main():
    current_app.logger.info("Admin {} has been signed in to admin console".format(current_user.email))
    return render_template('admin/dashboard.html')


@admin.route('/school', methods=['GET', 'POST'])
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
    return render_template('admin/school_list.html', schools=schools, current_schools_only=True)


@admin.route('/school/all', methods=['GET', 'POST'])
@roles_required('admin')
def school_all_list():
    schools = School.query.filter_by().all()
    return render_template('admin/school_list.html', schools=schools, current_schools_only=False)


@admin.route('school/<school_id>', methods=['GET', 'POST'])
@roles_required('admin')
def school_info(school_id):
    current_school = School.query.filter_by(id=school_id).first()
    if current_school:
        return render_template('admin/school_info.html', school=current_school)
    else:
        flash("School with id " + str(school_id) + " did not find", "danger")
        return redirect(url_for('admin.school_list'))


@admin.route('school/add', methods=['GET', 'POST'])
@roles_required('admin')
def school_add():
    form = SchoolForm()
    if form.validate_on_submit():
        new_school = School()
        form.populate_obj(new_school)
        # save new school to db
        db.session.add(new_school)
        db.session.commit()
        flash(new_school.name + " created", "success")
        return redirect(url_for('admin.school_list'))
    else:
        return render_template('admin/school_add_edit.html', form=form, action='add')


@admin.route('school/<school_id>/edit', methods=['GET', 'POST'])
@roles_required('admin')
def school_edit(school_id):
    current_school = School.query.filter_by(id=school_id).first()
    form = SchoolForm()
    if form.validate_on_submit():
        form.populate_obj(current_school)
        # save to db
        db.session.commit()
        flash(current_school.name + " edited", "success")
        return redirect(url_for('admin.school_list'))
    else:
        if current_school:
            form = SchoolForm(obj=current_school)
            return render_template('admin/school_add_edit.html', form=form, action='edit', school=current_school)
        else:
            flash("School with id " + str(school_id) + " did not find", "danger")
            return redirect(url_for('admin.school_list'))


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


@admin.route('/user', methods=['GET', 'POST'])
@roles_required('admin')
def user_list():
    # users = Role.query.filter_by(name='admin').first().users  # admins only
    users = User.query.all()
    return render_template('admin/user_list.html', users=users)


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
