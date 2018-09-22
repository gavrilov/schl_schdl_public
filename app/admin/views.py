from flask import render_template, Blueprint, current_app
from flask_security import current_user, roles_required

from app.models import Student

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def main():
    current_app.logger.info("Admin {} has been signed in to admin console".format(current_user.email))
    return render_template('admin/dashboard.html')





@admin.route('/students', methods=['GET', 'POST'])
@roles_required('admin')
def student_list():
    students = Student.query.all()
    return render_template('admin/student_list.html', students=students)
