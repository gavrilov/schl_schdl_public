from flask import render_template, Blueprint, flash, redirect, url_for, current_app, request
from flask_security import current_user, login_required, roles_required

from app import db, user_datastore
from app.models import User, UserContacts, Student, Role, School, Teacher
from app.payment import my_cards, my_payments
from app.school.forms import SchoolListForm
from app.user.forms import UserForm, UserContactForm, UserSettingsForm

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def user_list():
    users = User.query.all()
    return render_template('user/dashboard/list.html', users=users, current_users_only=True)


@user.route('/all', methods=['GET', 'POST'])
@roles_required('admin')
def user_all_list():
    users = User.query.all()
    return render_template('user/dashboard/list.html', users=users, current_users_only=False)


@user.route('/add', methods=['GET', 'POST'])
@roles_required('admin')
def user_add():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User()
        form.populate_obj(new_user)
        # save new school to db
        db.session.add(new_user)
        db.session.commit()
        flash("User {} {} created".format(new_user.first_name, new_user.last_name), "success")
        return redirect(url_for('user.user_list'))
    else:
        return render_template('user/dashboard/add.html', form=form, action='add')


@user.route('/<user_id>', methods=['GET', 'POST'])
@roles_required('admin')
def user_info(user_id):
    thisuser = User.query.filter_by(id=user_id).first()
    if thisuser:
        return render_template('user/dashboard/info.html', user=thisuser)
    else:
        flash("User with id {} did not find".format(user_id), "danger")
        return redirect(url_for('user.user_list'))


@user.route('/role', methods=['POST'])
@roles_required('admin')
def user_role():
    # TODO add token to this form
    action = request.form['action']
    role = request.form['role']
    user_id = request.form['user_id']

    thisuser = User.query.filter_by(id=user_id).first()
    thisrole = Role.query.filter_by(name=role).first()
    if thisuser and thisrole:
        if action == 'add':
            user_datastore.add_role_to_user(thisuser, thisrole)
            if thisrole.name == 'teacher' and not Teacher.query.filter_by(id=thisuser.id).first():
                new_teacher = Teacher()
                new_teacher.user_id = thisuser.id
                db.session.add(new_teacher)
                db.session.commit()


        elif action == 'remove':
            user_datastore.remove_role_from_user(thisuser, thisrole)
        db.session.commit()
        flash("{} {} updated".format(thisuser.first_name, thisuser.last_name), "success")
        return redirect(url_for('user.user_info', user_id=thisuser.id))
    else:
        flash("{} {} something wrong".format(thisuser.first_name, thisuser.last_name), "warning")
        return redirect(url_for('user.user_info', user_id=thisuser.id))


@user.route('/<user_id>/edit', methods=['GET', 'POST'])
@roles_required('admin')
def user_edit(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = UserForm()

    if form.validate_on_submit():
        form.populate_obj(user)
        # save to db
        db.session.commit()
        flash("User {} {} edited".format(user.first_name, user.last_name), "success")
        return redirect(url_for('dashboard.user_list'))
    else:
        if user:
            form = UserForm(obj=user)
            return render_template('user/dashboard/user_edit.html', form=form, user_id=user_id)
        else:
            flash("User with id {} did not find".format(user_id), "danger")
            return redirect(url_for('user.user_list'))


@user.route('/<user_id>/school', methods=['GET', 'POST'])
@roles_required('admin')
def user_school(user_id):
    thisuser = User.query.filter_by(id=user_id).first()
    current_schools = School.query.filter_by(current=True).all()

    form = SchoolListForm()
    # Now forming the list of tuples for SelectField
    school_list = [(i.id, i.name) for i in current_schools]
    form.school_id.choices = school_list

    if form.validate_on_submit():
        thisschool = School.query.filter_by(id=form.school_id.data).first()
        if thisschool:
            if thisuser not in thisschool.users:
                thisschool.users.append(thisuser)
                # save to db
                db.session.commit()
                flash("{} {} added to {}".format(thisuser.first_name, thisuser.last_name, thisschool.name), "success")
                return redirect(url_for('user.user_info', user_id=thisuser.id))
            else:
                flash("{} {} already connected to {}".format(thisuser.first_name, thisuser.last_name, thisschool.name),
                      "warning")
                return redirect(url_for('user.user_info', user_id=thisuser.id))
        else:
            flash("School with id {} does not find".format(form.school_id.data), 'danger')
    else:
        if thisuser:
            return render_template('user/dashboard/school.html', form=form, user=thisuser)
        else:
            flash("User with id {} did not find".format(user_id), "danger")
            return redirect(url_for('user.user_list'))


@user.route('/account', methods=['GET', 'POST'])
@login_required
def main():
    students = Student.query.filter_by(user_id=current_user.id).all()
    contacts = UserContacts.query.filter_by(user_id=current_user.id).all()
    cards_html = my_cards()
    payments_html = my_payments()

    if not contacts:
        flash("Please add your contact information", "danger")
        return redirect(url_for('user.add_contacts'))
    if not students:
        flash("Please add student information", "danger")
        return redirect(url_for('student.add_student'))
    return render_template('user/user_info.html', user=current_user, students=students, cards_html=cards_html,
                           payments_html=payments_html)


@user.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = UserSettingsForm()
    contacts = UserContacts.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit():
        form.populate_obj(current_user)
        # save to db
        db.session.commit()
        flash("User {} {} edited".format(current_user.first_name, current_user.last_name), "success")
        return redirect(url_for('user.main'))
    else:
        form = UserForm(obj=current_user)
        return render_template('user/edit.html', form=form, user_id=current_user.id, contacts=contacts)


@user.route('/contacts/add', methods=['GET', 'POST'])
@login_required
def add_contacts():
    form = UserContactForm()
    # form.state.data = 'TX'  # TODO default state of enrichment classes provider
    # form.contact_by_email.data = True  # doesn't work - you cannot change it in the form
    # form.contact_by_mail.data = True
    # form.contact_by_txt.data = True
    form.email.data = current_user.email

    if form.validate_on_submit():
        contact_info = UserContacts()
        form.populate_obj(contact_info)
        # save new school to db
        contact_info.user_id = current_user.id
        db.session.add(contact_info)
        db.session.commit()
        flash("Contact information updated", "success")
        return redirect(url_for('user.main'))

    if form.errors:
        print(form.errors)
        for error in form.errors.values():
            flash(error, 'danger')

    return render_template('user/contact_info.html', form=form)


@user.route('/contacts/<contact_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_contacts(contact_id):
    contact_info = UserContacts.query.filter_by(id=contact_id).first()

    if not contact_info or contact_info.user_id != current_user.id:
        current_app.logger.warning(
            'User is trying to edit not his contact. user_id = {} contact_id = {}'.format(current_user.id, contact_id))
        flash("Contact does not find", "danger")
        return redirect(url_for('user.main'))

    form = UserContactForm(obj=contact_info)

    if form.validate_on_submit():
        form.populate_obj(contact_info)
        # save new school to db
        contact_info.user_id = current_user.id
        db.session.commit()
        flash("Contact information updated", "success")
        return redirect(url_for('user.main'))

    if form.errors:
        print(form.errors)
        for error in form.errors.values():
            flash(error, 'danger')

    return render_template('user/contact_info.html', form=form, editing_existing_contact=True, contact_id=contact_id)


@user.route('/contacts/<contact_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_contacts(contact_id):
    contact_info = UserContacts.query.filter_by(id=contact_id).first()

    if not contact_info or contact_info.user_id != current_user.id:
        current_app.logger.warning(
            'User is trying to delete not his contact. user_id = {} contact_id = {}'.format(current_user.id,
                                                                                            contact_id))
        flash("Contact does not find", "danger")
        return redirect(url_for('user.main'))

    db.session.delete(contact_info)
    db.session.commit()
    flash("Contact has been deleted", "success")
    return redirect(url_for('user.main'))
