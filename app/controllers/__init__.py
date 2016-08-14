# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import abort
# from flask import flash
from flask import session
from flask.ext.moment import Moment
from ..models import User
from ..models import Bloglist
from ..models import Comment
from flask import jsonify
import log
from flask import Blueprint


main = Blueprint('controllers', __name__)


def current_user():
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    return user


@main.route('/visitor_login')
def visitor_login():
    user = User.query.filter_by(username='visitor').first()
    session['user_id'] = user.id
    r = redirect(url_for('.bloglist_view_all', username=user.username))
    return r


@main.route('/bloglist')
def bloglist_view_all():
    user = current_user()
    if user == None:
        abort(404)
    # u = User.query.filter_by(username=username).first()
    user_list = User.query.all()
    # log(u)
    # if u is None:
    #     abort(404)
    # log('currentuser', user)
    # log('user.id',user.id)
    # log('u.id', u.id)
    # log('u.bloglist', u.bloglist)
    # bloglist = u.bloglist
    # bloglist.sort(key=lambda t: t.created_time, reverse=True)
    # print(username, current_user().username)
    page = request.args.get('page', 1, type=int)
    pagination = Bloglist.query.order_by(Bloglist.created_time.desc()).paginate(page,
                                                                                      per_page=8,
                                                                                      error_out=False)
    posts = pagination.items
    print(posts)
    return render_template('bloglist.html', bloglist=posts, username='', cur_user=current_user(),
                           all_users=user_list,  pagination=pagination)


@main.route('/bloglist/<username>')
def bloglist_view(username):
    # sql = str(User.query.filter_by(username=username))
    # log(sql)
    u = User.query.filter_by(username=username).first()
    user_list = User.query.all()
    # log(u)
    if u is None:
        abort(404)
    user = current_user()
    # log('currentuser', user)
    # log('user.id',user.id)
    # log('u.id', u.id)
    # log('u.bloglist', u.bloglist)
    bloglist = u.bloglist
    bloglist.sort(key=lambda t: t.created_time, reverse=True)
    print(username, current_user().username)
    page = request.args.get('page', 1, type=int)
    pagination = Bloglist.query.filter_by(user_id=u.id).order_by(Bloglist.created_time.desc()).paginate(page,
                                                                                                        per_page=8,
                                                                                                        error_out=False)
    posts = pagination.items
    print(posts)
    return render_template('bloglist.html', bloglist=posts, username=username, cur_user=current_user(),
                           all_users=user_list,  pagination=pagination)


@main.route('/bloglist/<username>/<blog_id>')
def blog_detail(username, blog_id):
    u = User.query.filter_by(username=username).first()
    # log(u)
    cur_user = current_user()
    print(cur_user)
    if u is None:
        abort(404)
    print(cur_user.username)
    b = Bloglist.query.filter_by(id=blog_id).first_or_404()
    print(b)
    print('title', blog_id)
    c = Comment.query.filter_by(blog_id=blog_id).all()
    print('c', c)
    # print(c.poster)
    print(b)
    print(b.id)
    print('role',cur_user.role)
    return render_template('artical.html', cur_user=cur_user, username=username, b=b, c=c)


@main.route('/publish')
def fabiao():
    return render_template('edit.html', action='publish', b=None)


@main.route('/update/<blog_id>')
def update_view(blog_id):
    b = Bloglist.query.filter_by(id=blog_id).first_or_404()
    return render_template('edit_update.html', b=b, action=True)











