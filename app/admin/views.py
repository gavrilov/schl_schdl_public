from flask import render_template, Blueprint, redirect, url_for, current_app
from flask_login import current_user, login_required

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/', methods=['GET', 'POST'])
@login_required
def main():
    if current_user.username not in current_app.config['ADMIN_USERNAME']:
        current_app.logger.warning(
            "User {} with id = {} is trying to get admin access".format(current_user.username, current_user.id))
        return redirect(url_for('user.main'))
    current_app.logger.info("Admin {} has been signed in to admin console".format(current_user.username))
    return render_template('admin/dashboard.html')
