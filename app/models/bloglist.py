from . import db
from . import ReprMixin

from datetime import datetime


class Bloglist(db.Model, ReprMixin):
    __tablename__ = 'bloglists'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=50))
    content = db.Column(db.String())
    preview = db.Column(db.String())
    created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    #comment = db.relationship('Comment', backref='poster')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.preview = form.get('summary', '')


    def json(self):
        # Model 是延迟载入的, 如果没有引用过数据, 就不会从数据库中加载
        # 引用一下 id 这样数据就从数据库中载入了
        self.id
        extra = dict(
            type='user',
        )
        d = {k:v for k,v in self.__dict__.items() if k not in self.blacklist()}
        d.update(extra)
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
        ]
        return b


    def save(self):
        db.session.add(self)
        db.session.commit()


    def update(self, form):
        print('tweet.update, ', form)
        new_title = form['title']
        new_content = form['content']
        new_preview = form['summary']
        self.content = new_content
        self.title = new_title
        self.preview = new_preview
        self.update_time = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()