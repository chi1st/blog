from ..models import User
from . import main
from flask import redirect
from flask import url_for

@main.route('/user/delete/<username>')
def user_delete(username):
    u = User.query.filter_by(username=username).first()
    print(u.username)
    u.delete()
    r = redirect(url_for('controllers.bloglist_view_all'))
    return r