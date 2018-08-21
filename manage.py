from app import create_app

from app.database import db
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate


app = create_app('C:/Projects/flask-easypost/config_dev.py')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, models=models)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    #app.run()

