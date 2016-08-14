from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment

# 暴露 db 是因为 models 要使用它
# 但是这时候还没有 app 所以要在 app 初始化之后再初始化这个 db
db = SQLAlchemy()


# 把 flask 的初始化放到函数中
# 由外部启动函数来调用
#
def init_app():
    db_path = 'db1.sqlite'

    # 初始化并配置 flask
    app = Flask(__name__)
    # 这一行 加了就没 warning(
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # 设置你的加密 key
    app.secret_key = 'TODO fixme'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    # 初始化 db
    # 相当于db = SQLAlchemy(app)但是这时候还没有 app 所以要在 app 初始化之后再初始化这个 db
    db.init_app(app)# 初始化app
    db.app = app# 把app赋值给db的app(套路)
    # # flask-moment , 在前端格式化时间
    moment = Moment(app)

    # 必须在函数中 import 蓝图
    # 否则循环引用(因为蓝图中 import 了 model, model 引用了这个文件里面目的 db)
    from .auth import auth as auth
    from .controllers import main as controllers
    from .api import main as api

    # 注册蓝图
    app.register_blueprint(auth)
    app.register_blueprint(controllers)
    app.register_blueprint(api, url_prefix='/api')

    # 把 app 引用返回
    return app

