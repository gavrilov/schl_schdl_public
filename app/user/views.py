from flask import request, render_template, Blueprint, flash, redirect, url_for, make_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.models import User, UserContacts, Student
from .forms import UserForm, EmailCheckForm, SignInForm, RegistrationForm, UserContactForm

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/', methods=['GET', 'POST'])
@login_required
def main():
    students = Student.query.filter_by(user_id=current_user.id).all()
    contacts = UserContacts.query.filter_by(user_id=current_user.id).all()
    print(contacts)
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
    form.email.data = current_user.username
    if form.validate_on_submit():
        contact_info = UserContacts()
        form.populate_obj(contact_info)
        # save new school to db
        contact_info.user_id = current_user.id
        db.session.add(contact_info)
        db.session.commit()
        flash("Contact information created", "success")
        return redirect(url_for('user.main'))
    else:
        return render_template('user/contact_info.html', form=form)

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


@user.route('/email', methods=['GET', 'POST'])
def email_check():
    form = EmailCheckForm()
    if form.validate_on_submit():
        user_exist = User.query.filter_by(username=form.username.data).first()
        if user_exist:
            flash('Parent exist. Please Login or Reset Password', 'warning')
            resp = make_response(redirect(url_for('user.sign_in')))
            resp.set_cookie('username', form.username.data)
            return resp
        else:
            flash('Email sent. Please go to link to confirm your email address', 'success')
            resp = make_response(redirect(url_for('user.register')))
            resp.set_cookie('username', form.username.data)
            return resp
    return render_template('user/email_check.html', form=form)


@user.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.main'))
    form = RegistrationForm()
    form.username.data = request.cookies.get('username')
    if form.validate_on_submit():
        new_user = User()
        new_user.username = form.username.data
        new_user.first_name = form.first_name.data
        new_user.last_name = form.last_name.data
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('user.sign_in'))
    return render_template('user/register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('user.main'))
    form = SignInForm()
    form.username.data = request.cookies.get('username')
    if form.validate_on_submit():
        this_user = User.query.filter_by(username=form.username.data).first()
        if this_user is None or not this_user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('user.sign_in'))
        login_user(this_user, remember=form.remember_me.data)
        flash('Hello!', 'success')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user.main')
        return redirect(next_page)
    return render_template('user/sign_in.html', form=form)


@user.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You have successfully logged out. Buy-Buy!', 'success')
    return redirect(url_for('hello_world'))


@user.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = SignInForm()
    form.username.data = request.cookies.get('username')
    if form.validate_on_submit():
        flash('Please contact with admin, that form does not work yet!', 'danger')
        return render_template('user/sign_in.html', form=form)
    return render_template('user/sign_in.html', form=form)
