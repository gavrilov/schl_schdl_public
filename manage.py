from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager, Shell

from app import create_app, db
from config import Config

app = create_app(config_class=Config)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    # TODO shell context and manager commands
    # return dict(app=app, db=db, models=models)
    return True


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    # app.run()
