"""
File: manage.py
Purpose: manager for the application
"""

from flask_script import Manager
from sweep import app, db, models

app.config.from_object('config.BaseConfiguration')

manager = Manager(app)


@manager.command
def createdb():
    '''Creates the database

       Ideally this would be using flask-migrate.
       But that's out of scope for now.
    '''
    db.create_all()


@manager.shell
def make_shell_context():
    ''' Returns app, db, models to the shell '''
    return dict(app=app, db=db, models=models)


if __name__ == "__main__":
    manager.run()
