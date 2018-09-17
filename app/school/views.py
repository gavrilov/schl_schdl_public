from flask import Blueprint

school = Blueprint('school', __name__, template_folder='templates')


@school.route('/', methods=['GET', 'POST'])
def main():
    return "School blueprint"
