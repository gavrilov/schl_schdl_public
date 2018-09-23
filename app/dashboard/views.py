from flask import render_template, Blueprint, current_app
from flask_security import current_user, roles_required

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def main():
    current_app.logger.info("Admin {} has been signed in to admin console".format(current_user.email))
    return render_template('dashboard/dashboard.html')
