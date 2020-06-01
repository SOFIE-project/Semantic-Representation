# !/usr/bin/env python
import sys
sys.path.append(".")
from project import create_app, db
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = '5000'


def server_startup():
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])


def server_shutdown():
    db.session.remove()
    db.drop_all()


if __name__ == '__main__':
    server_startup()
    server_shutdown()