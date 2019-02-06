import datetime
import json

import pytz as tz
from dateutil import rrule
from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_babelex import _
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
    # current_teachers = Teacher.query.filter_by(current=True).all()

    # Now forming the list of tuples for SelectField
    # teacher_list = [(i.id, i.user.first_name + " " + i.user.last_name) for i in current_teachers]

    # form.school_id.choices = school_list
    # form.teacher_id.choices = teacher_list
    return render_template('event/edit_popup.html', form=form, current_event=current_event)


@event.route('/', methods=['GET', 'POST'])
@roles_required('admin')
def event_list():
    events = Event.query.filter(Event.schdl_class.has(current=True)).order_by(Event.start.asc()).all()
    # TODO current_events_only - by date or Schdl_Class.current = True. if today in range(start_date_of_class, end_date_of_class)
    return render_template('event/event_list.html', events=events, current_events_only=False)


@event.route('/add/class/<class_id>', methods=['GET', 'POST'])
@roles_required('admin')
def add_event(class_id):
    current_class = Schdl_Class.query.filter_by(id=class_id).first()
    if current_class.events.first():
        flash(_('Current class already has events'), 'warning')
        # temporary disabled check for existing events
        # return redirect(url_for('event.list_for_class', class_id=current_class.id))
        return create_events(current_class)
    return create_events(current_class)


@event.route('/class/<class_id>', methods=['GET', 'POST'])
@roles_required('admin')
def list_for_class(class_id):
    current_class = Schdl_Class.query.filter_by(id=class_id).first()
    events = current_class.events.order_by(Event.start.asc()).all()
    return render_template('event/event_list.html', events=events, current_class=current_class)


@event.route('/add/<class_id>', methods=['GET', 'POST'])
@roles_required('admin')
def add_event_for_class(class_id):
    current_class = Schdl_Class.query.filter_by(id=class_id).first()
    if not current_class:
        flash(_('Class did not find'), 'danger')
        return redirect(url_for('event.list_for_class', class_id=class_id))
    form = PopupEventForm()

    current_teachers = Teacher.query.filter_by(current=True).all()

    # Now forming the list of tuples for SelectField
    teacher_list = [(i.id, i.user.first_name + " " + i.user.last_name) for i in current_teachers]

    form.teacher_id.choices = teacher_list

    if form.validate_on_submit():
        form.class_id.data = current_class.id
        current_event = Event()
        form.populate_obj(current_event)
        # save to db
        db.session.add(current_event)
        db.session.commit()
        flash(_('Event has been added'), 'success')
        return redirect(url_for('event.list_for_class', class_id=class_id))
    else:
        return render_template('event/add.html', form=form, current_class=current_class)


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
            flash(_('Event has been updated'), 'success')
            return redirect(url_for('event.event_list'))
        else:
            return render_template('event/edit.html', form=form, current_event=current_event)
    else:
        flash(_('Event did not find'), 'danger')
        return redirect(url_for('event.event_list'))


@event.route('/delete/<event_id>', methods=['GET', 'POST'])
@roles_required('admin')
def delete_event(event_id):
    # TODO check attendance that connect with this event, told user that he should delete them first
    current_event = Event.query.filter_by(id=event_id).first()
    current_class = current_event.schdl_class
    if current_event:
        db.session.delete(current_event)
        db.session.commit()
        flash(_('Event has been deleted'), 'success')
        return redirect(url_for('event.list_for_class', class_id=current_class.id))
    else:
        flash(_('Event did not find'), 'danger')
        return redirect(url_for('event.event_list'))


@event.route('/data/<schdl_object>/<id>', methods=['GET', 'POST'])
def data(schdl_object, id):
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    current_time_zone = request.args.get('timezone', '')

    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    time_zone = tz.timezone(current_time_zone)

    if schdl_object == 'class':
        current_class = Schdl_Class.query.filter_by(id=id).first()
        events = current_class.events.filter(Event.start > start, Event.end < end).all()
        return generate_calendar_data(events, time_zone)
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
        return generate_calendar_data(events, time_zone)
        pass

    return 'ok'


def generate_calendar_data(events, time_zone):
    json_data = []
    for current_event in events:
        json_data.append(dict_from_event(current_event, time_zone))
    # print(json_data)
    return json.dumps(json_data)


def dict_from_event(current_event, time_zone):
    event_data = {}
    event_data['id'] = current_event.id
    event_data['start'] = current_event.start.astimezone(time_zone).isoformat()
    event_data['end'] = current_event.end.astimezone(time_zone).isoformat()
    event_data['active'] = current_event.active
    title_teachers = ''
    for teacher in current_event.schdl_class.teachers:
        title_teachers += '{} {}; '.format(teacher.user.first_name, teacher.user.last_name)
    title = '<s>{} @ {} - {}</s>'.format(current_event.schdl_class.subject.name,
                                         current_event.schdl_class.school.name,
                                         title_teachers)

    if not current_event.active:
        event_data['title'] = '<s>{}</s>'.format(title)
        event_data['color'] = '#ff0000'
    else:
        event_data['title'] = '{}'.format(title)
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

    if not start or not end:
        flash(_('Class does not have start or end date'), 'warning')
        return redirect(url_for('schdl_class.edit_class', class_id=current_class.id))

    if not current_class.class_time_start or not current_class.class_time_end:
        flash(_('Class does not have start or end time'), 'warning')
        return redirect(url_for('schdl_class.edit_class', class_id=current_class.id))

    if current_class.payrate is None or current_class.billing_rate is None:
        flash(_('Class does not have Pay or Billing rate'), 'warning')
        return redirect(url_for('schdl_class.edit_class', class_id=current_class.id))
    # https://stackoverflow.com/questions/43305577/python-calculate-the-difference-between-two-datetime-time-objects
    # To calculate the difference - convert the datetime.time object to a datetime.datetime
    start_time = datetime.datetime.combine(start, current_class.class_time_start)
    end_time = datetime.datetime.combine(start, current_class.class_time_end)
    # calculate last date of class and end time
    end_date = datetime.datetime.combine(end, current_class.class_time_end)

    # get seconds from timedelta object and divide
    class_duration = (end_time - start_time).total_seconds()

    # add info about current time zone
    time_zone = tz.timezone('America/Chicago')
    start_time_local = time_zone.localize(start_time)

    end_local = time_zone.localize(end)
    # convert to utc timezone
    # start_time_utc = start_time_local.astimezone(tz.utc)
    # end_time_utc = end_local.astimezone(tz.utc)
    # print(start_time_local.strftime('%m/%d/%Y %I:%M %p'))

    # generate without time zone
    event_dates = rrule.rrule(rrule.WEEKLY, dtstart=start_time, until=end_date)
    for event_date in event_dates:
        new_event = Event()
        new_event.class_id = current_class.id
        new_event.active = True
        # add time zone and convert to utc
        new_event.start = time_zone.localize(event_date).astimezone(tz.utc)
        new_event.end = new_event.start + datetime.timedelta(seconds=class_duration)
        new_event.teacher_id = current_class.teacher.id
        new_event.payrate = current_class.payrate
        new_event.billing_rate = current_class.billing_rate
        db.session.add(new_event)
    db.session.commit()
    flash(_('Events have been created'), 'success')
    return redirect(url_for('schdl_class.edit_class', class_id=current_class.id))
