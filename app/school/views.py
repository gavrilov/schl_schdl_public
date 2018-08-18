from flask import Flask, request, render_template, session, Blueprint, flash, redirect, url_for
from app import db


school = Blueprint('school', __name__, template_folder='templates')


@school.route('/', methods=['GET', 'POST'])
def main():
    return render_template('school/main_page.html')

