import secrets

from flask import render_template, Blueprint, flash, redirect, url_for, current_app, request
from flask_babelex import _
from flask_security import current_user, login_required, roles_required, url_for_security
from flask_security.recoverable import generate_reset_password_token
from flask_security.registerable import register_user

from app import db, user_datastore
from app.models import User, UserContacts, Student, Role, School, Teacher, Enrollment
from app.payment import my_cards, my_payments
from app.payment.forms import PaymentForm
from app.school.forms import SchoolListForm
from app.tools import send_email_to_user
from app.user.forms import UserForm, UserContactForm, UserSettingsForm

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def user_list():
    q = db.session.query(User)
    users = q.filter(User.students.any(Student.enrollments.any(Enrollment.schdl_class.has(current=True))))
    return render_template('user/dashboard/list.html', users=users, current_users_only=True)


@user.route('/all', methods=['GET', 'POST'])
@roles_required('admin')
def user_all_list():
    users = User.query.all()
    return render_template('user/dashboard/list.html', users=users, current_users_only=False)


@user.route('/without_students', methods=['GET', 'POST'])
@roles_required('admin')
def user_without_students_list():
    # show students who are not enrolled in any classes
    q = db.session.query(User)
    users = q.filter(~User.students.any())  # ~ means not
    return render_template('user/dashboard/list.html', users=users, current_users_only=False)


@user.route('/add', methods=['GET', 'POST'])
@roles_required('admin')
def user_add():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash(_('{email} is already associated with another user').format(email=email), 'danger')
            form.email.data = ''
            return render_template('user/dashboard/add.html', form=form, action='add')
        else:
            # generate random password
            password = secrets.token_urlsafe(16)
            first_name = form.first_name.data
            last_name = form.last_name.data
            note = form.note.data
            new_user = register_user(first_name=first_name, last_name=last_name, note=note, email=email,
                                     password=password)
            flash(_('User has been created'), 'success')

            # if send invitation is checked - send email with link to reset password
            if form.send_email.data is True:
                token = generate_reset_password_token(new_user)
                reset_link = url_for_security('reset_password', token=token, _external=True)
                send_email_to_user(user=new_user, msg_subject='Invitation',
                                   msg_html=render_template('emails/invitation.html', user=new_user,
                                                            reset_link=reset_link))
            return redirect(url_for('user.user_info', user_id=new_user.id))
    else:
        return render_template('user/dashboard/add.html', form=form, action='add')


@user.route('/<user_id>', methods=['GET', 'POST'])
@roles_required('admin')
def user_info(user_id):
    thisuser = User.query.filter_by(id=user_id).first()

    if not thisuser:
        flash(_('User did not find'), 'danger')
        return redirect(url_for('user.user_list'))

    form = PaymentForm()
    form.user_id.data = thisuser.id
    payments_html = my_payments(thisuser)
    cards_html = my_cards(thisuser)
    return render_template('user/dashboard/info.html', user=thisuser, payments_html=payments_html,
                           cards_html=cards_html, form=form)



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
            if thisrole.name == 'teacher' and not Teacher.query.filter_by(user_id=thisuser.id).first():
                new_teacher = Teacher()
                new_teacher.user_id = thisuser.id
                db.session.add(new_teacher)
                db.session.commit()
                flash(_('Teacher created'), 'success')

        elif action == 'remove':
            user_datastore.remove_role_from_user(thisuser, thisrole)
        db.session.commit()
        flash(_('User has been updated'), 'success')
        return redirect(url_for('user.user_info', user_id=thisuser.id))
    else:
        flash(_('Something wrong'), 'warning')
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
        flash(_('User has been updated'), 'success')
        return redirect(url_for('dashboard.user_list'))
    else:
        if user:
            form = UserForm(obj=user)
            return render_template('user/dashboard/user_edit.html', form=form, user_id=user_id)
        else:
            flash(_('User did not find'), 'danger')
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
                flash(_('User has been added to School'), 'success')
                return redirect(url_for('user.user_info', user_id=thisuser.id))
            else:
                flash(_('User already connected to School'), 'warning')
                return redirect(url_for('user.user_info', user_id=thisuser.id))
        else:
            flash(_('School did not find'), 'danger')
    else:
        if thisuser:
            return render_template('user/dashboard/school.html', form=form, user=thisuser)
        else:
            flash(_('User did not find'), 'danger')
            return redirect(url_for('user.user_list'))


@user.route('/account', methods=['GET', 'POST'])
@login_required
def main():
    students = Student.query.filter_by(user_id=current_user.id).all()
    contacts = UserContacts.query.filter_by(user_id=current_user.id).all()
    cards_html = my_cards()
    payments_html = my_payments()

    if not contacts:
        flash(_('Please add your contact information'), 'danger')
        return redirect(url_for('user.add_contacts'))
    if 'teacher' in current_user.roles and 'admin' not in current_user.roles:
        return redirect(url_for('dashboard.teacher_dashboard'))
    if not students:  # TODO filter for admins and parents and not (current_user.has_role('admin') or current_user.has_role('teacher')):
        flash(_('Please add student information'), 'danger')
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
        flash(_('User has been updated'), 'success')
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
        flash(_('Contact information has been updated'), 'success')
        return redirect(url_for('user.main'))

    if form.errors:
        print(form.errors)
        for error in form.errors.values():
            flash(error, 'danger')

    return render_template('user/contact_info.html', form=form, step=1)  # step=1 for progress bar


@user.route('/contacts/<contact_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_contacts(contact_id):
    contact_info = UserContacts.query.filter_by(id=contact_id).first()
    if not contact_info or (contact_info not in current_user.contacts and not current_user.has_role(
            'admin')):
        current_app.logger.warning(
            'User is trying to edit not his contact. user_id = {} contact_id = {}'.format(current_user.id, contact_id))
        flash(_('Contact information did not find'), 'danger')
        return redirect(url_for('user.main'))

    form = UserContactForm(obj=contact_info)

    if form.validate_on_submit():
        form.populate_obj(contact_info)
        db.session.commit()
        flash(_('Contact information has been updated'), 'success')
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

    if not contact_info or (contact_info not in current_user.contacts and not current_user.has_role(
            'admin')):
        current_app.logger.warning(
            'User is trying to delete not his contact. user_id = {} contact_id = {}'.format(current_user.id,
                                                                                            contact_id))
        flash(_('Contact information did not find'), 'danger')
        return redirect(url_for('user.main'))

    db.session.delete(contact_info)
    db.session.commit()
    flash(_('Contact information has been deleted'), 'success')
    return redirect(url_for('user.main'))
