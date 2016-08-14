from ..models import Bloglist
from . import main
from . import current_user
from flask import request
from flask import abort
from flask import jsonify
from flask import url_for


@main.route('/bloglist/delete/<bloglist_id>')
def bloglist_delete(bloglist_id):
    t = Bloglist.query.filter_by(id=bloglist_id).first()
    if t is None:
        abort(404)
    # 获取当前登录的用户, 如果用户没登录或者用户不是这条的主人, 就返回 401 错误
    user = current_user()
    if user is None :
        abort(401)
    else:
        t.delete()
        print('t', t)
        # return redirect(url_for('bloglist_view', username=user.username))
        r = {
            'success': True,
            'message': '删除成功',
        }
        return jsonify(r)


@main.route('/tweet/add', methods=['POST'])
def tweet_add():
    print('hahha')
    u = current_user()
    print(u.username)
    print(u)
    form = request.get_json()
    print(form)
    t = Bloglist(form)
    t.user = u
    # timeArray = time.localtime(t.created_time)
    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # t.created_time = otherStyleTime
    t.save()
    print(t.created_time)
    r = dict(
        success=True,
        data=t.json(),
    )
    print(url_for('controllers.bloglist_view', username=u.username))
    r['next'] = request.args.get('next', url_for('controllers.blog_detail', username=u.username, blog_id=t.id))
    print('r', r)
    return jsonify(r)


@main.route('/tweet/update/<blog_id>', methods=['POST'])
def update(blog_id):
    u = current_user()
    b = Bloglist.query.filter_by(id=blog_id).first_or_404()
    form = request.get_json()
    print(form)
    b.update(form)
    print(b)
    r = dict(
        success=True,
        data=b.json(),
    )
    r['next'] = request.args.get('next', url_for('controllers.bloglist_view', username=u.username))
    print('r', r)
    return jsonify(r)

