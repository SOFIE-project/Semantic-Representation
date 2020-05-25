from project import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    schemas = db.relationship('TDSchema', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __str__(self):
        return self.username

    def get_user_id(self):
        return self.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class TDSchema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    schema_name = db.Column(db.String(40), unique=True)
    schema = db.Column(db.String(2048))

    def __repr__(self):
        return '<Schema {}>'.format(self.schema_name)
