from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    username = db.Column(db.String(30), index=True, unique=True)
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)
    tasks = db.relationship('TaskList', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Hashing the password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class TaskList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    body = db.Column(db.Text())
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<TaskList {}>'.format(self.title)

    def is_own_task(self, id):
        if id == current_user.id:
            return True
        return False


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
