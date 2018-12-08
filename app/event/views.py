import datetime
import json

import pytz as tz
from dateutil import rrule
from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_security import roles_required

from app import db
from app.models import Event, Schdl_Class, Teacher
from .forms import PopupEventForm

event = Blueprint('event', __name__, template_folder='templates')


@event.route('/popup', methods=['GET', 'POST'])
@roles_required('admin')
def generate_popup_url():
    # We need it to generate a base of dynamic url for popups
    return False


@event.route('/popup/<event_id>/', methods=['GET', 'POST'])
@roles_required('admin')
def generate_popup_html(event_id):
    current_event = Event.query.filter_by(id=event_id).first()
    form = PopupEventForm(obj=current_event)
    current_teachers = Teacher.query.filter_by(current=True).all()

    # Now forming the list of tuples for SelectField
    teacher_list = [(i.id, i.user.first_name + " " + i.user.last_name) for i in current_teachers]

    # form.school_id.choices = school_list
    form.teacher_id.choices = teacher_list
    return render_template('event/edit_popup.html', form=form, current_event=current_event)


@event.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def event_list():
    events = Event.query.filter_by().all()
    # TODO current_events_only - by date or Schdl_Class.current = True. if today in range(start_date_of_class, end_date_of_class)
    return render_template('event/event_list.html', events=events, current_events_only=False)


@event.route('/add/class/<class_id>', methods=['GET', 'POST'])
@roles_required('admin')
def add_event(class_id):
    current_class = Schdl_Class.query.filter_by(id=class_id).first()
    event_dates = create_events(current_class)

    flash('Events for {} class at {} have been created'.format(current_class.subject.name, current_class.school.name),
          'success')
    return 'Ok'


@event.route('/edit/<event_id>', methods=['GET', 'POST'])
@roles_required('admin')
def edit_event(event_id):
    current_event = Event.query.filter_by(id=event_id).first()
    if current_event:
        form = PopupEventForm(obj=current_event)

        current_teachers = Teacher.query.filter_by(current=True).all()

        # Now forming the list of tuples for SelectField
        teacher_list = [(i.id, i.user.first_name + " " + i.user.last_name) for i in current_teachers]

        # form.school_id.choices = school_list
        form.teacher_id.choices = teacher_list

        if form.validate_on_submit():
            form.populate_obj(current_event)
            # save to db
            db.session.commit()
            flash("Event of {} class at {} has been updated".format(current_event.schdl_class.subject.name,
                                                                    current_event.schdl_class.school.name), "success")
            return redirect(url_for('event.event_list'))
        else:
            return render_template('event/edit.html', form=form, current_event=current_event)
    else:
        flash("Event with id {} did not find".format(event_id), "danger")
        return redirect(url_for('event.event_list'))


@event.route('/data/<schdl_object>/<id>', methods=['GET', 'POST'])
def data(schdl_object, id):
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')

    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    if schdl_object == 'class':
        current_class = Schdl_Class.query.filter_by(id=id).first()
        events = current_class.events.filter(Event.start > start, Event.end < end).all()
        return generate_calendar_data(events)
    elif schdl_object == 'student':
        # get Events between star_date & end_date for student_id
        pass
    elif schdl_object == 'user':
        # get Events between star_date & end_date for user_id
        pass
    elif schdl_object == 'teacher':
        # get Events between star_date & end_date for teacher_id
        pass
    elif schdl_object == 'school':
        # get Events between star_date & end_date for school_id
        pass
    elif schdl_object == 'all':
        # get all Events between star_date & end_date
        events = Event.query.filter(Event.start > start, Event.end < end).all()
        return generate_calendar_data(events)
        pass

    return 'ok'


def generate_calendar_data(events):
    json_data = []
    for current_event in events:
        json_data.append(dict_from_event(current_event))
    print(json_data)
    return json.dumps(json_data)


def dict_from_event(current_event):
    event_data = {}
    event_data['id'] = current_event.id
    event_data['start'] = current_event.start.isoformat()
    event_data['end'] = current_event.end.isoformat()
    event_data['active'] = current_event.active
    if not current_event.active:
        event_data['title'] = '<s>{} @ {} - {} {}</s>'.format(current_event.schdl_class.subject.name,
                                                              current_event.schdl_class.school.name,
                                                              current_event.schdl_class.teacher.user.first_name,
                                                              current_event.schdl_class.teacher.user.last_name)
        event_data['color'] = '#ff0000'
    else:
        event_data['title'] = '{} @ {} - {} {}'.format(current_event.schdl_class.subject.name,
                                                       current_event.schdl_class.school.name,
                                                       current_event.schdl_class.teacher.user.first_name,
                                                       current_event.schdl_class.teacher.user.last_name)
        event_data['color'] = current_event.schdl_class.subject.color
    if current_event.payrate:
        event_data['payrate'] = float(current_event.payrate)
    if current_event.billing_rate:
        event_data['billing_rate'] = float(current_event.billing_rate)
    event_data['note'] = current_event.note
    return event_data


def create_events(current_class):
    # dates of start and end
    start = current_class.class_start
    end = current_class.class_end
    # TODO if not start or not end: error
    # https://stackoverflow.com/questions/43305577/python-calculate-the-difference-between-two-datetime-time-objects
    # To calculate the difference - convert the datetime.time object to a datetime.datetime
    start_time = datetime.datetime.combine(start, current_class.class_time_start)
    end_time = datetime.datetime.combine(start, current_class.class_time_end)
    # TODO if not start or not end: error
    # get seconds from timedelta object and divide
    class_duration = (end_time - start_time).total_seconds()

    # add info about current time zone
    time_zone = tz.timezone('America/Chicago')
    start_time_local = time_zone.localize(start_time)

    end_local = time_zone.localize(end)
    # convert to utc timezone
    # start_time_utc = start_time_local.astimezone(tz.utc)
    # print(start_time_local.strftime('%m/%d/%Y %I:%M %p'))

    event_dates = rrule.rrule(rrule.WEEKLY, dtstart=start_time_local, until=end_local)

    for event_date in event_dates:
        new_event = Event()
        new_event.class_id = current_class.id
        new_event.active = True
        new_event.start = event_date
        new_event.end = event_date + datetime.timedelta(seconds=class_duration)
        new_event.teacher_id = current_class.teacher.id
        new_event.payrate = current_class.payrate
        new_event.billing_rate = current_class.billing_rate
        db.session.add(new_event)
    db.session.commit()

    return True
