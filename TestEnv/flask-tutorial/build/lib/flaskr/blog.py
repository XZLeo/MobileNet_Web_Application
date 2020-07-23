from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)
#与验证蓝图不同，博客蓝图没有 url_prefix 。因此 index 视图会用于 / ， create 会用于 /create ，以此类推。
#博客是 Flaskr 的主要 功能，因此把博客索引作为主索引是合理的。

@bp.route('/')
def index():
    """索引视图  
    功能：
    会显示所有帖子，最新的会排在最前面
    权限：
    游客可以查看"""
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username\
          FROM post AS p JOIN user AS u ON p.author_id = u.id \
          ORDER BY created DESC;'
    ).fetchall()   
    #fetchall返回元组的列表，fetchone返回单个元组
    #print(posts) #元组的list，要转换成dict的list
    key = ("id", "title", "body", "created", "author_id", "username")
    a= []
    for post in posts:
        a.append(dict(zip(key, post)))

    return render_template('blog/index.html', posts=a)
  

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """游客必须登录才能查看"""
    #print('fdsafsd')
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        #print(g.user)
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else: #没出错则将博客插入数据库,并回到index界面
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                'VALUES (?, ?, ?)',
                (title, body, g.user[0]) #g.user['id']
            )
            db.commit()
            return redirect(url_for('blog.index')) #？？
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    """update 和 delete 视图都需要通过 id 来获取一个 post ，并且 检查作者与登录用户是否一致。"""
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username\
            FROM post AS p JOIN user AS u\
            ON p.author_id=u.id\
            WHERE p.id=?',
        (id,)
        #如果此user也存在于author表中，就表明他是author
    ).fetchone() #1 tuple

    if post is None:
        abort(404, "Post id {0} does not exist.".format(id))
    else:
        key = ("id", "title", "body", "created", "author_id", "username")
        post = dict(zip(key, post))

    if check_author and post['author_id'] != g.user[0]: #g.user['id']
        #函数可以用于在不检查作者的情况下获取一个 post 
        #这主要用于显示一个独立的帖子页面的情况，因为这时用户是谁没有关系， 用户不会修改帖子。
        abort(403)
    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """
    Input: id 对应路由中 的 <int:id>,是博客的id
    """
    #print("1234")
    post = get_post(id)  #最后传入模板显示

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?\
                    WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('GET', 'POST')) #改成get就不会405了
@login_required
def delete(id):
    #print("dsfa")
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id=?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
    

    #为什么会出现大规模的tuple和dict混淆？
    # delete和update为什么用不了？
    #删除blog后id不会自动更改，很不方便，因为我不知道每个blog的id
    #访问这个url没起到效果http://127.0.0.1:5000/4/delete
    #