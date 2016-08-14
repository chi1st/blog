from . import db
from . import ReprMixin
import time
import hashlib
from datetime import datetime

def conver_to_hash(content):
    hash = hashlib.sha1(content.encode('utf-8')).hexdigest()
    return hash


class User(db.Model, ReprMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.Integer, default=2)
    bloglist = db.relationship('Bloglist', backref='user')

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = conver_to_hash((form.get('password', '')))


    def is_admin(self):
        return self.role == 1

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def valid(self):
        username_len = len(self.username) >= 3
        password_len = len(self.password) >= 3
        return username_len and password_len

    def validate(self, user):
        if isinstance(user, User):
            username_equals = self.username == user.username
            password_equals = self.password == user.password
            return username_equals and password_equals
        else:
            return False

    def valid_unique_existence(self):
        user = User.query.filter_by(username=self.username).first()
        if user == None:
            return True
        else:
            return False
