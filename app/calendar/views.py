from flask import Flask, request, render_template, session, Blueprint, flash, redirect, url_for
from app import db


calendar = Blueprint('calendar', __name__, template_folder='templates')


@calendar.route('/', methods=['GET', 'POST'])
def main():
    return render_template('calendar/main_page.html')

@calendar.route('/data', methods=['GET', 'POST'])
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    # You'd normally use the variables above to limit the data returned
    # you don't want to return ALL events like in this code
    # but since no db or any real storage is implemented I'm just
    # returning data from a text file that contains json elements

    with open("app/calendar/events.json", "r") as input_data:
        # you should use something else here than just plaintext
        # check out jsonfiy method or the built in json module
        # http://flask.pocoo.org/docs/0.10/api/#module-flask.json
        return input_data.read()
