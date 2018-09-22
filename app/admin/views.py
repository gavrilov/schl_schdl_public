from flask import render_template, Blueprint, current_app, redirect, url_for, flash
from flask_security import current_user, roles_required

from app import db
from app.admin.forms import UserForm
from app.models import User, Student

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def main():
    current_app.logger.info("Admin {} has been signed in to admin console".format(current_user.email))
    return render_template('admin/dashboard.html')


@admin.route('/user/<user_id>/edit', methods=['GET', 'POST'])
@roles_required('admin')
def user_edit(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = UserForm()

    if form.validate_on_submit():
        form.populate_obj(user)
        # save to db
        db.session.commit()
        flash("User {} {} edited".format(user.first_name, user.last_name), "success")
        return redirect(url_for('admin.user_list'))
    else:
        if user:
            form = UserForm(obj=user)
            return render_template('admin/user_edit.html', form=form, user_id=user_id)
        else:
            flash("User with id {} did not find".format(user_id), "danger")
            return redirect(url_for('admin.user_list'))


@admin.route('/students', methods=['GET', 'POST'])
@roles_required('admin')
def student_list():
    students = Student.query.all()
    return render_template('admin/student_list.html', students=students)
