import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth') 
#指定了这个蓝图的URL前缀/auth

""" 这里创建了一个名称为 'auth' 的 Blueprint 。和应用对象一样， 蓝图需要知道是在哪里定义的，
因此把 __name__ 作为函数的第二个参数。 url_prefix 会添加到所有与该蓝图关联的 URL 前面

认证蓝图将包括3个视图：注册新用户、登录和注销

视图是一个应用对请求进行响应的函数，Blueprint 是一种组织一组相关视图及其他代码的方式
 """

@bp.route('/register', methods=('GET', 'POST')) #当 Flask 收到一个指向 /auth/register 的请求时就会调用 register 视图并把其返回值作为响应。
def register():
    """注册视图"""
    #print("艹")
    #print(request.method)
    if request.method == 'POST': #提交表单
        #print("艹1")
        username = request.form['username']
        password = request.form['password']
        db = get_db()  # 创建数据库连接 
        error = None   # 没有用c= conn.cursor()去调用execute

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registred.'.format(username)
        
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)', #为了安全原因，不能把密码明文 储存在数据库中
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login')) #url_for() 函数最简单的用法是以视图函数名作为参数，返回对应的url

        flash(error)
    #print("你")    
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
       #print(dir(g.user))
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        #print("到")
        # # user = query_db(
        # #     'SELECT * FROM user WHERE username = ?',
        # #     (username,)
        # # )
        # print("一")
        user = db.execute(
            'SELECT * FROM user WHERE username=?', (username,)
        ).fetchone()
        #避免带有先验知识的硬编码！！
        
        #print(user)
        if user is None:
            error = 'Incorrect username.'
        # elif  not check_password_hash(user['password'], password):
        elif  not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        
        flash(error)
      
    return render_template('auth/login.html')

 
@bp.before_app_request   
def load_logged_in_user():
    """ 用于储存横跨请求的值。当验证 成功后，用户的 id 被储存于一个新的会话中。
        会话数据被储存到一个 向浏览器发送的 cookie 中，在后继请求中，浏览器会返回它 """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
    return 

@bp.route('/logout')
def logout():
    """注销的时候需要把用户 id 从 session 中移除。
       然后 load_logged_in_user 就不会在后继请求中载入用户了"""
    session.clear()
    return redirect(url_for('index'))

def login_required(view): 
    """view代表其他视图函数，函数作为参数
       这个装饰器将会在博客蓝图中使用"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

#这里有问题！！！！index界面点击new之后循环

#为什么是db是get_db的返回值  涉及到flask的g对象
# 函数的装饰器、函数中定义函数
# 调用函数，函数内部定义的函数总是会被调用。。可能这里是为了使用装饰器

# Flask view functions must return either a Response object or a string. To fix your code, add return "" at the end of index() 
# 视图函数要么返回render_template 要么返回

#fetchone和fetchall的不同
#(2, 'XZL', 'pbkdf2:sha256:150000$tJipFFo9$289581d25d6fd6ef22976e47a493138c3870d6dae16c35b45944e2285367d102')