from app import init_app
from app import models


def rebuild_db():
    # 必须初始化 app 才能操作数据库
    app = init_app()
    db = models.db
    db.drop_all()
    db.create_all()
    print('auth rebuild database')


def run():
    config = dict(
        # host='0.0.0.0',
        port=9990,
        debug=True,
    )
    init_app().run(**config)


if __name__ == '__main__':
    # rebuild_db()
    run()

