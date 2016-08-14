from flask import request
from flask import url_for
from flask import jsonify
from flask import session
from flask import Blueprint
from ..models import Bloglist
from ..models import Comment
from flask import abort

from functools import wraps

from ..models import User


main = Blueprint('api', __name__)

def current_user():
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    return user

from . import blog
from . import comment
from . import user


