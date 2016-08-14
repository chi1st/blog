# -*- coding: utf-8 -*-
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import session
from flask import Blueprint

from ..models import User
import log

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    return redirect(url_for('.login_view'))


@auth.route('/login')
def login_view():
    return render_template('login.html')


@auth.route('/logout')
def logoout():
    session['user_id'] = None
    return redirect(url_for('.login_view'))


@auth.route('/login', methods=['Post'])
def login():
    u = User(request.form)
    print('u', u)
    print('u.username', u.username, u.password)
    user = User.query.filter_by(username=u.username).first()
    x = User.query.filter(User.username != 'admin').all()
    print('x', x)
    print('user', user)
    # print('user.username',user.username)
    # log(user)
    # log(user.validate(u))
    if user == None:
        # log('用户登录失败')
        flash('此用户不存在')
        # return redirect(url_for
        return '此用户不存在'
    elif user.validate(u):
        # log('用户登录成功')
        session['user_id'] = user.id
        print('session', session)
        r = redirect(url_for('controllers.bloglist_view_all', username=user.username))
        print('r', r)
        # cookie_id = str(uuid.uuid4())
        # cookie_dict[cookie_id] = user
        # r.set_cookie('cookie_id', cookie_id)
        # return r
        return r
    else:
        # log('用户登录失败')
        flash('用户密码错误')
        # return redirect(url_for('login_view'))
        return '用户密码错误'


@auth.route('/register', methods=['POST'])
def register():
    u = User(request.form)
    # log(u)
    # log(u.valid())
    # log(u.valid_unique_existence())
    if u.valid() and u.valid_unique_existence():
        flash('注册成功')
        # log('用户注册成功')
        u.save()
        # return redirect(url_for('login_view'))
        return redirect(url_for('.login_view'))
    else:
        flash('失败')
        # log('注册失败', request.form)
        # return redirect(url_for('login_view'))
        return '注册失败'