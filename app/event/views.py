from flask import Flask, request, render_template, session, Blueprint, flash, redirect, url_for
from app import db
from .forms import EventForm
from app.models import Schdl_Class
from app.models import School
from app.models import Teacher
from app.models import Event

event = Blueprint('event', __name__, template_folder='templates')


@event.route('/', methods=['GET', 'POST'])
def main():
    events = Event.query.filter_by().all()
    # TODO current_events_only - by date or Schdl_Class.current = True. if today in range(start_date_of_class, end_date_of_class)
    return render_template('event/event_list.html', events=events, current_events_only=False)


@event.route('/add', methods=['GET', 'POST'])
def add_event():
    #current_schools = School.query.filter_by(current=True).all()
    current_teachers = Teacher.query.filter_by(current=True).all()
    current_classes = Schdl_Class.query.filter_by(current=True).all()
    form = EventForm()

    # Now forming the list of tuples for SelectField
    #school_list = [(i.id, i.name) for i in current_schools]
    teacher_list = [(i.id, i.first_name + " " + i.last_name) for i in current_teachers]
    class_list = [(i.id, i.school.name + " - " + i.subject.name) for i in current_classes]

    # passing group_list to the form
    # form.school_id.choices = school_list
    form.teacher_id.choices = teacher_list
    form.class_id.choices = class_list
    if form.validate_on_submit():
        new_event = Event()
        form.populate_obj(new_event)
        # save new school to db
        db.session.add(new_event)
        db.session.commit()
        flash("Event for " + new_event.teacher.first_name + " at " + new_event.schl_class.school.name + " created", "success")
        return redirect(url_for('event.main'))
    else:
        return render_template('event/add.html', form=form)


@event.route('/edit/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    current_event = Event.query.filter_by(id=event_id).first()
    if current_event:
        form = EventForm(obj=current_event)

        #current_schools = School.query.filter_by(current=True).all()
        current_teachers = Teacher.query.filter_by(current=True).all()
        current_classes = Schdl_Class.query.filter_by(current=True).all()

        # Now forming the list of tuples for SelectField
        #school_list = [(i.id, i.name) for i in current_schools]
        teacher_list = [(i.id, i.first_name + " " + i.last_name) for i in current_teachers]
        class_list = [(i.id, i.school.name + " - " + i.subject.name) for i in current_classes]

        #form.school_id.choices = school_list
        form.teacher_id.choices = teacher_list
        form.class_id.choices = class_list

        if form.validate_on_submit():
            form.populate_obj(current_event)
            #save to db
            db.session.commit()
            flash(current_event.schl_class.school.name + " event edited", "success")
            return redirect(url_for('event.main'))
        else:
            return render_template('event/edit.html', form=form, event_id=event_id)
    else:
        flash("Event with id " + str(event_id) + " did not find", "danger")
        return redirect(url_for('event.main'))
