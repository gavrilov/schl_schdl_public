from flask import Flask, request, render_template, session, Blueprint, flash, redirect, url_for
from app import db
from .forms import ClassForm

schdl_class = Blueprint('schdl_class', __name__, template_folder='templates')

@schdl_class.route('popup', methods=['GET', 'POST'])
def generate_popup_url():
    # We need it to generate a base of dynamic url for popups
    return False

@schdl_class.route('popup/<class_id>/', methods=['GET', 'POST'])
def generate_popup_html(class_id):
    print('I GOT IT!', class_id)
    form = ClassForm()
    form.title.data = class_id
    return render_template('schdl_class/edit.html', form=form)



