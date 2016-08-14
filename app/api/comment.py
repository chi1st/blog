from ..models import Bloglist
from . import main
from . import current_user
from ..models import Comment
from flask import request
from flask import abort
from flask import jsonify


@main.route('/comment/add/<blog_id>', methods=['POST'])
def bloglist_comment(blog_id):
    user = current_user()
    c = Comment(request.get_json())
    # 设置是谁评论的
    print('c', c.comment_content)
    c.poster = user.username
    c.blog_id = blog_id
    # timeArray = time.localtime(c.created_time)
    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # c.created_time = otherStyleTime
    # 保存到数据库
    c.save()
    print(c.created_time)
    counts = Comment.query.filter_by(blog_id=blog_id).count()
    print(counts)
    r = dict(
        success=True,
        data=c.json(),
        counts=counts
    )
    print('r', r)
    print('json', jsonify(r))
    return jsonify(r)


@main.route('/comment/delete/<comment_id>')
def comment_delete(comment_id):
    c = Comment.query.filter_by(id=comment_id).first()
    if c is None:
        abort(404)
    # 获取当前登录的用户, 如果用户没登录或者用户不是这条的主人, 就返回 401 错误
    user = current_user()
    if user is None:
        abort(401)
    else:
        c.delete()
        print('c', c)
        # return redirect(url_for('bloglist_view', username=user.username))
        counts = Comment.query.filter_by(blog_id=c.blog_id).count()
        print(counts)
        r = {
            'success': True,
            'message': '删除成功',
            'counts': counts
        }
        return jsonify(r)
