from flask import render_template, Blueprint, flash, redirect, url_for
from flask_security import roles_required, current_user

from app import db
from app.models import User, Student, Teacher, Enrollment

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def main():
    # Dashboard for Admins
    users = db.session.query(User).count()
    students = db.session.query(Student).count()
    enrollments_num = db.session.query(Enrollment).count()
    five_last_enrollments = db.session.query(Enrollment).order_by(Enrollment.id.desc()).limit(5).all()
    return render_template('dashboard/dashboard.html', users=users, students=students, enrollments_num=enrollments_num,
                           five_last_enrollments=five_last_enrollments)


@dashboard.route('/teacher', methods=['GET', 'POST'])
@roles_required('teacher')
def teacher_dashboard():
    # Dashboard for teachers
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher or not teacher.current:
        flash('Teacher does not find. Please contact administration')
        return redirect(url_for('hello_world'))
    return render_template('dashboard/dashboard_teacher.html', teacher=teacher)
