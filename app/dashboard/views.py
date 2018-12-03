from flask import render_template, Blueprint, flash, redirect
from flask_security import roles_required, current_user

from app import db
from app.models import User, Student, Teacher

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def main():
    users = db.session.query(User).count()
    students = db.session.query(Student).count()
    return render_template('dashboard/dashboard.html', users=users, students=students)


@dashboard.route('/teacher', methods=['GET', 'POST'])
@roles_required('teacher')
def teacher_dashboard():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher or not teacher.current:
        flash('Teacher does not find. Please contact administration')
        return redirect('hello_world')
    return render_template('dashboard/dashboard_teacher.html', teacher=teacher)
