from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.shellplus import Shell


app = Flask(__name__)
db = SQLAlchemy(app)
manager = Manager(app)


def make_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_context))


if __name__ == '__main__':
    manager.run()
