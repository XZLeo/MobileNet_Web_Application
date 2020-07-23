import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # 创建数据库连接
    if 'db' not in g: 
        #g是对象,保存当前请求的各种信息,此处g的db属性用于保存数据库连接
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], #配置文件中DATABASE接指向配置中的 DATABASE 指定的文件。这个文件现在还没有建立，后面会在初始化数据库的时候建立该文件。
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        #如果连接已存在则什么也不干
        #为什么没有使用cursor
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()
    return

# def query_db(query, args=(), one=False):
#     """execute结果转换成dict，原本返回tuple,专门用于改写SELECT语句"""
#     print("此")
#     # cur = db.execute(query, args).fetchall()
#     # print(cur)
#     db = get_db()
#     cur = db.execute(query, args)

#     rv = []
#     for row in cur.fetchall():
#         for idx, value in enumerate(row):
#             rv = [dict((cur.description[idx][0], value))]
#     rv = [dict((cur.description[idx][0], value)
#                for idx, value in enumerate(row)) for row in cur.fetchall()]
#     print(rv)
#     return (rv[0] if rv else None) if one else rv

def init_db():
    
    db = get_db() #创建连接
    #print("motherfucker")
    #读入脚本建表
    with current_app.open_resource('./schema.sql') as f: #文件名都相对于flaskr
        #print("mother")
        db.executescript(f.read().decode('utf8'))
        db.executescript(f.read().decode('utf8'))
    return

@click.command('initdb')
@with_appcontext
def init_db_command():
    # 定义一个名为 init-db 命令行，它调用 init_db 函数，并为用户显示一个成功的消息
    #clear the existing data and create new tables
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    #app实例中注册
    app.teardown_appcontext(close_db) #告诉 Flask 在返回响应后进行清理的时候调用此函数
    app.cli.add_command(init_db_command) #添加一个新的 可以与 flask 一起工作的命令


#不只是建立一次链接，而是要app能反复调用数据库
    














#g对象，把连接储存于其中，可以多次使用，
# 而不用在同一个 请求中每次调用 get_db 时都创建一个新的连接
# g为什么有那么多属性可以直接用？

# current_app 是另一个特殊对象，该对象指向处理请求的 Flask 应用。
# 这里 使用了应用工厂，那么在其余的代码中就不会出现应用对象。
# 当应用创建后，在处理 一个请求时， get_db 会被调用。