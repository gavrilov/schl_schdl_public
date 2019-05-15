from datetime import datetime

from flask import render_template, Blueprint, flash, redirect, url_for, current_app, request
from flask_babelex import _
from flask_security import current_user, login_required, roles_required, roles_accepted
from sqlalchemy import and_

from app import db
from app.models import Student, Schdl_Class, School, Semester
from .forms import StudentForm

student = Blueprint('student', __name__, template_folder='templates')


@student.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def student_list():
    semesters = Semester.query.filter_by(current=True).all()
    students_html = ""
    current_classes = Schdl_Class.query.filter_by(current=True).all()
    for current_class in current_classes:
        for enrollment in current_class.enrollments:
            print(enrollment.student_id)
        # generate rows for table for each class
        students_html += render_template('student/student_list_rows.html', current_class=current_class)
    return render_template('student/student_list.html', students_html=students_html, current_students_only=True,
                           semesters=semesters)


@student.route('/semester/<semester_id>', methods=['GET', 'POST'])
@roles_required('admin')
def student_list_by_semester(semester_id):
    semesters = Semester.query.filter_by(current=True).all()
    students_html = ""
    current_classes = Schdl_Class.query.filter_by(current=True, semester_id=semester_id).all()
    for current_class in current_classes:
        # generate rows for table for each class
        students_html += render_template('student/student_list_rows.html', current_class=current_class)
    return render_template('student/student_list.html', students_html=students_html, current_students_only=True,
                           semesters=semesters)


@student.route('/drops', methods=['GET', 'POST'])
@roles_required('admin')
def student_drops_list():
    semesters = Semester.query.filter_by(current=True).all()
    students_html = ""
    current_classes = Schdl_Class.query.filter_by(current=True).all()
    for current_class in current_classes:
        # generate rows for table for each class
        students_html += render_template('student/student_drops_list_rows.html', current_class=current_class)
    return render_template('student/student_list.html', students_html=students_html, drops_students_only=True,
                           semesters=semesters)


@student.route('/drops/semester/<semester_id>', methods=['GET', 'POST'])
@roles_required('admin')
def student_drops_list_by_semester(semester_id):
    semesters = Semester.query.filter_by(current=True).all()
    students_html = ""
    current_classes = Schdl_Class.query.filter_by(current=True, semester_id=semester_id).all()
    for current_class in current_classes:
        # generate rows for table for each class
        students_html += render_template('student/student_drops_list_rows.html', current_class=current_class)
    return render_template('student/student_list.html', students_html=students_html, drops_students_only=True,
                           semesters=semesters)


@student.route('/all', methods=['GET', 'POST'])
@roles_required('admin')
def student_all_list():
    # show all students who enrolled in any classes or dropped
    students = Student.query.filter(Student.enrollments.any())
    return render_template('student/student_list_not_current.html', students=students)


@student.route('/not_enrolled', methods=['GET', 'POST'])
@roles_required('admin')
def not_enrolled():
    # show students who are not enrolled in any classes
    students = Student.query.filter(~Student.enrollments.any()).order_by(Student.timestamp.desc()).all()

    return render_template('student/student_list_not_current.html', students=students)


@student.route('/<student_id>', methods=['GET', 'POST'])
@roles_required('admin')
def info(student_id):
    current_student = Student.query.filter_by(id=student_id).first()
    if current_student:
        return render_template('student/student_info.html', student=current_student)
    else:
        flash(_('Student did not find'), 'danger')
        return redirect(url_for('student.student_list'))


@student.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    current_schools = School.query.filter_by(current=True, hide_from_users=False).order_by(School.name.asc()).all()
    # Now forming the list of tuples for SelectField
    school_list = [(i.id, i.name) for i in current_schools]

    form = StudentForm()
    form.default_school_id.choices = [(0, "---")]+school_list
    if form.validate_on_submit():
        new_student = Student()
        form.dob.data = datetime.strptime('{}/{}/{}'.format(form.dob_month.data, form.dob_day.data, form.dob_year.data),
                                          '%m/%d/%Y')
        form.populate_obj(new_student)
        current_user.students.append(new_student)
        db.session.commit()
        flash(_('Student has been created'), 'success')
        return redirect(url_for('student.enroll_student', student_id=new_student.id))

    if form.errors:
        for error in form.errors.values():
            flash(error, 'danger')

    return render_template('student/add.html', form=form, step=2)  # step=2 for progressbar


@student.route('/<student_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    current_student = Student.query.filter_by(id=student_id).first()
    if not current_student or (current_student not in current_user.students and not current_user.has_role(
            'admin')):  # TODO or current_student not in current_user.students
        current_app.logger.warning(
            'User is trying to edit not his student. user_id = {} student_id = {}'.format(current_user.id, student_id))
        flash(_('Student does not find'), 'danger')
        return redirect(url_for('user.main'))
    current_schools = School.query.filter_by(current=True, hide_from_users=False).order_by(School.name.asc()).all()
    # Now forming the list of tuples for SelectField
    school_list = [(i.id, i.name) for i in current_schools]
    form = StudentForm(obj=current_student)
    form.default_school_id.choices = [(0, "---")] + school_list

    if form.validate_on_submit():
        form.dob.data = datetime.strptime('{}/{}/{}'.format(form.dob_month.data, form.dob_day.data, form.dob_year.data),
                                          '%m/%d/%Y')
        form.populate_obj(current_student)
        # save to db
        db.session.commit()
        flash(_('Student has been updated'), 'success')
        return redirect(url_for('user.main'))

    form.dob_month.data = form.dob.data.strftime("%m")
    form.dob_day.data = form.dob.data.strftime("%d")
    form.dob_year.data = form.dob.data.strftime("%Y")

    return render_template('student/edit.html', form=form, student_id=student_id)


@student.route('/<student_id>/delete', methods=['GET', 'POST'])
@roles_required('admin')
def delete_student(student_id):
    current_student = Student.query.filter_by(id=student_id).first()
    current_user = current_student.user
    if not current_student or (current_student not in current_user.students and not current_user.has_role(
            'admin')):  # TODO or current_student not in current_user.students
        current_app.logger.warning(
            'User is trying to edit not his student. user_id = {} student_id = {}'.format(current_user.id, student_id))
        flash(_('Student does not find'), 'danger')
        return redirect(url_for('user.main'))
    db.session.delete(current_student)
    db.session.commit()
    flash(_('Student has been deleted'), 'info')
    return redirect(url_for('user.user_info', user_id=current_user.id))


@student.route('/<student_id>/enroll', methods=['GET', 'POST'])
@login_required
def enroll_student(student_id):
    # list all classes available for current_student
    current_student = Student.query.filter_by(id=student_id).first()
    if not current_student or (current_student not in current_user.students and not current_user.has_role('admin')):
        current_app.logger.warning(
            'User is trying to enroll not his student. user_id = {} student_id = {}'.format(current_user.id,
                                                                                            student_id))
        flash(_('Student does not find'), 'danger')
        return redirect(url_for('user.main'))
    current_school = School.query.filter_by(id=current_student.default_school_id).first()
    current_classes = current_school.classes.filter_by(current=True).order_by(Schdl_Class.day_of_week.asc(), Schdl_Class.class_time_start.asc()).all()
    enrolled_classes = Schdl_Class.query.filter(and_(Schdl_Class.enrollments.any(student_id=current_student.id),
                                                     Schdl_Class.enrollments.any(current=True))).all()
    utc_now = datetime.utcnow()
    return render_template('student/enroll.html', current_classes=current_classes, student=current_student,
                           current_school=current_school, enrolled_classes=enrolled_classes, utc_now=utc_now,
                           step=3)  # step=3 for progressbar


@student.route('/edit_note', methods=['GET', 'POST'])
@roles_accepted('admin')
def edit_note():
    name = request.form['name']
    note = request.form['value']
    student_id = request.form['pk']
    if student_id:
        current_student = Student.query.filter_by(id=student_id).first()
        if current_student:
            current_student.note = note
            db.session.commit()
        return render_template('page.html'), 200
    else:
        return render_template('page.html'), 404


@student.route('/student_processing', methods=['GET', 'POST'])
@roles_required('admin')
def student_processing():
    if request.method == 'POST':
        # for send mass emails and txt msgs
        # TODO csrf_token to ajax request
        action = request.form['action']
        students_ids = request.form.getlist('students')
        students = []
        if students_ids:
            for student_id in students_ids:
                this_student = Student.query.filter_by(id=student_id).first()
                if this_student:
                    students.append(this_student)
        if action == "labels":
            return render_template('student/address_labels.html', students=students)
        if action == "email":
            emails = []
            for this_student in students:
                for contact in this_student.user.contacts:
                    if contact.email:
                        emails.append(contact.email)
                    else:
                        emails.append(this_student.user.email)
            uniq_emails = set(emails)
            emails = list(uniq_emails)
            email_href_string = ','.join(emails)
            email_string = '; '.join(emails)
            email_link = '<a href="mailto:?bcc={email_href_string}">{email_string}</a>'.format(
                email_href_string=email_href_string, email_string=email_string)
            return render_template('student/email.html', email_link=email_link)
        if action == "txt":
            phone_numbers = []
            for this_student in students:
                for contact in this_student.user.contacts:
                    if contact.phone:
                        phone_numbers.append(contact.phone)
            uniq_emails = set(phone_numbers)
            phone_numbers = ",".join(str(x) for x in list(phone_numbers))
            url = '<a href="{url}">{text2}</a>'.format(
                url=url_for('txtmsg.send_msg', phone_numbers=phone_numbers, _external=True), text2=_('Click to send'))
            print(url)

            return url
    else:
        return render_template('page.html'), 404
