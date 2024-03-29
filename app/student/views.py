from datetime import datetime
import operator
from flask import render_template, Blueprint, flash, redirect, url_for, current_app, request
from flask_babelex import _
from flask_security import current_user, login_required, roles_required, roles_accepted
from sqlalchemy import and_

from app import db
from app.models import Student, Schdl_Class, School, Semester, Note
from .forms import StudentForm, StudentFormDashboard

student = Blueprint('student', __name__, template_folder='templates')


@student.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def student_list():
    semesters = Semester.query.all()
    students_html = ""
    current_classes = Schdl_Class.query.filter_by(current=True).join(Semester, Schdl_Class.semester).filter_by(show_in_list=True).all()
    for current_class in current_classes:
        # generate rows for table for each class
        students_html += render_template('student/student_list_rows.html', current_class=current_class)
    return render_template('student/student_list.html', students_html=students_html, current_students_only=True,
                           semesters=semesters)


@student.route('/semester/<semester_id>', methods=['GET', 'POST'])
@roles_required('admin')
def student_list_by_semester(semester_id):
    semesters = Semester.query.all()
    current_semester = Semester.query.filter_by(id=semester_id).first()
    students_html = ""
    current_classes = Schdl_Class.query.filter_by(current=True, semester_id=semester_id).all()
    for current_class in current_classes:
        # generate rows for table for each class
        students_html += render_template('student/student_list_rows.html', current_class=current_class)
    return render_template('student/student_list.html', students_html=students_html, current_students_only=True,
                           semesters=semesters, current_semester=current_semester)


@student.route('/drops', methods=['GET', 'POST'])
@roles_required('admin')
def student_drops_list():
    semesters = Semester.query.all()
    students_html = ""
    current_classes = Schdl_Class.query.filter_by(current=True).join(Semester, Schdl_Class.semester).filter_by(show_in_list=True).all()
    for current_class in current_classes:
        # generate rows for table for each class
        students_html += render_template('student/student_drops_list_rows.html', current_class=current_class)
    return render_template('student/student_list.html', students_html=students_html, drops_students_only=True,
                           semesters=semesters)


@student.route('/drops/semester/<semester_id>', methods=['GET', 'POST'])
@roles_required('admin')
def student_drops_list_by_semester(semester_id):
    semesters = Semester.query.all()
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
    from dateutil.relativedelta import relativedelta

    if current_student:
        age = round(abs((current_student.dob - datetime.utcnow()).total_seconds() / 31536000), 1)
        return render_template('student/student_info.html', student=current_student, age=age)
    else:
        flash(_('Student did not find'), 'danger')
        return redirect(url_for('student.student_list'))


@student.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():

    # Create list of current School, that not hided from user and in current semester
    current_schools = []  # School.query.filter_by(current=True, hide_from_users=False).order_by(School.name.asc()).all()
    current_semesters = Semester.query.filter_by(current=True).all()
    for semester in current_semesters:
        for current_class in semester.classes:
            if current_class.current and current_class.school.current and not current_class.school.hide_from_users and current_class.school not in current_schools:
                current_schools.append(current_class.school)
    current_schools.sort(key=operator.attrgetter('name'))

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

    # Create list of current School, that not hided from user and in current semester
    current_schools = [] # School.query.filter_by(current=True, hide_from_users=False).order_by(School.name.asc()).all()
    current_semesters = Semester.query.filter_by(current=True).all()
    for semester in current_semesters:
        for current_class in semester.classes:
            if current_class.current and current_class.school.current and not current_class.school.hide_from_users and current_class.school not in current_schools:
                current_schools.append(current_class.school)

    if current_user.has_role('admin'):
        current_schools = School.query.all()
        form = StudentFormDashboard(obj=current_student)
    else:
        form = StudentForm(obj=current_student)

    current_schools.sort(key=operator.attrgetter('name'))

    # Now forming the list of tuples for SelectField
    school_list = [(i.id, i.name) for i in current_schools]



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

    if current_user.has_role('admin'):
        return render_template('dashboard/student/edit.html', form=form, student_id=student_id)
    else:
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

    return render_template('student/enroll.html', current_classes=current_classes, student=current_student,
                           current_school=current_school, enrolled_classes=enrolled_classes,
                           step=3)  # step=3 for progressbar


@student.route('/edit_note', methods=['GET', 'POST'])
@roles_accepted('admin')
def edit_note():
    name = request.form['name']
    note = request.form['value']
    note_id = request.form['pk']
    student_id = name.split('-')[2]
    print(note_id)
    if note_id != '0':
        current_note = Note.query.filter_by(id=note_id).first()
        if current_note:
            current_note.text = note
            db.session.commit()
        return render_template('page.html'), 200

    elif note_id == '0':
        current_student = Student.query.filter_by(id=student_id).first()
        print(current_student.first_name)
        if current_student:
            current_note = Note()
            current_note.text = note
            current_student.notes.append(current_note)
            db.session.commit()
            return render_template('page.html'), 200
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


@student.route('/dance', methods=['GET', 'POST'])
@roles_required('admin')
def student_dance_list():
    semesters = Semester.query.all()
    students_html = ""
    current_classes = Schdl_Class.query.filter_by(current=True).filter_by(subject_id=1).join(Semester, Schdl_Class.semester).filter_by(show_in_list=True).all()
    for current_class in current_classes:
        # generate rows for table for each class
        students_html += render_template('student/dance/student_list_rows.html', current_class=current_class)
    return render_template('student/dance/student_list.html', students_html=students_html, current_students_only=True,
                           semesters=semesters)

