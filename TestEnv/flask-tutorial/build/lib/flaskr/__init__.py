import os
from flask import Flask

def create_app(test_config=None):
    """create and configure the app""" 
    app = Flask(__name__, instance_relative_config=True)
    #print(__name__) #说明name就是flaskr
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)

    #ensure the instance folder exists
    # Flask 不会自动 创建实例文件夹，但是必须确保创建这个文件夹，因为 SQLite 数据库文件会被 保存在里面
    try:
        # print(app.instance_path) # E:\Intern\WebMachine\flask-tutorial\instance
        os.makedirs(app.instance_path) 
    except OSError:
        print('OSError')

    #a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from .db import init_app #在工厂中导入db.py并调用init-db,导入没有问题
    init_app(app)
    
    #导入并注册auth蓝图
    from . import auth
    app.register_blueprint(auth.bp) #auth模块的bp函数

    #导入并注册blog蓝图
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    #对于更复杂的项目，每个蓝图对应一个文件夹，都分别有自己的init，然后在整个项目的init中分别注册
    


    return app
    #必须返回app才能被flask找到！！！



    

'''
__name__ 是当前 Python 模块的名称。应用需要知道在哪里设置路径， 使用 __name__ 是一个方便的方法。
__init__.py是flaskr包中负责导入其他module
'''

#包含应用工厂
#flaskr文件夹应当视作为一个包。
# set FLASK_APP = flaskr
# set FLASK_ENV = development
# flask run
# 有空格也没事每次都进入flask-tutorial目录运行