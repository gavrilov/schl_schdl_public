from flask import render_template, Blueprint
from flask_security import roles_required

from app import db
from app.models import User, Student

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def main():
    users = db.session.query(User).count()
    students = db.session.query(Student).count()
    return render_template('dashboard/dashboard.html', users=users, students=students)
