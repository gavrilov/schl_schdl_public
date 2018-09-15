from flask import render_template, Blueprint, flash, redirect, url_for, current_app
from flask_security import current_user, login_required

from app import db
from app.models import User, UserContacts, Student
from app.user.forms import UserForm, UserContactForm

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/', methods=['GET', 'POST'])
@login_required
def main():
    students = Student.query.filter_by(user_id=current_user.id).all()
    contacts = UserContacts.query.filter_by(user_id=current_user.id).all()
    if not contacts:
        flash("Please add your contact information", "danger")
        return redirect(url_for('user.add_contacts'))
    if not students:
        flash("Please add students", "danger")
        return redirect(url_for('student.add_student'))
    return render_template('user/user_info.html', user=current_user, students=students, contacts=contacts)


@user.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    form = UserForm()
    if form.validate_on_submit():
        form.populate_obj(current_user)
        # save to db
        db.session.commit()
        flash(current_user.first_name + " " + current_user.last_name + " edited", "success")
        return redirect(url_for('user.main'))
    else:
        form = UserForm(obj=current_user)
        return render_template('user/edit.html', form=form, user_id=current_user.id)


@user.route('/contacts/add/', methods=['GET', 'POST'])
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


@user.route('/contacts/edit/<contact_id>', methods=['GET', 'POST'])
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


@user.route('/contacts/delete/<contact_id>', methods=['GET', 'POST'])
@login_required
def delete_contacts(contact_id):
    contact_info = UserContacts.query.filter_by(id=contact_id).first()

    if not contact_info or contact_info.user_id != current_user.id:
        current_app.logger.warning(
            'User is trying to delete not his contact. user_id = {} contact_id = {}'.format(current_user.id,
                                                                                            contact_id))
        flash("Contact does not find", "danger")
        flash("Contact does not find", "danger")
        return redirect(url_for('user.main'))

    db.session.delete(contact_info)
    db.session.commit()
    flash("Contact has been deleted", "success")
    return redirect(url_for('user.main'))


@user.route('/all', methods=['GET', 'POST'])
def user_list():
    users = User.query.all()
    return render_template('user/user_list.html', users=users, current_users_only=False)


@user.route('/<user_id>', methods=['GET', 'POST'])
def info(user_id):
    current_user = User.query.filter_by(id=user_id).first()
    if current_user:
        return render_template('user/user_info.html', user=current_user)
    else:
        flash("Parent with id " + str(user_id) + " did not find", "danger")
        return redirect(url_for('user.main'))


@user.route('/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User()
        form.populate_obj(new_user)
        # save new school to db
        db.session.add(new_user)
        db.session.commit()
        flash(new_user.first_name + " " + new_user.last_name + " created", "success")
        return redirect(url_for('user.main'))
    else:
        return render_template('user/add.html', form=form)


@user.route('/edit/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    current_user = User.query.filter_by(id=user_id).first()
    form = UserForm()
    if form.validate_on_submit():
        form.populate_obj(current_user)
        # save to db
        db.session.commit()
        flash(current_user.first_name + " " + current_user.last_name + " edited", "success")
        return redirect(url_for('user.main'))
    else:
        if current_user:
            form = UserForm(obj=current_user)
            return render_template('user/edit.html', form=form, user_id=user_id)
        else:
            flash("Parent with id " + str(user_id) + " did not find", "danger")
            return redirect(url_for('user.main'))
