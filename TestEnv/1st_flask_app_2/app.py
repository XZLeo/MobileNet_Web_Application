from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators

app = Flask(__name__)

class HelloForm(Form):
    sayhello = TextAreaField('', [validators.DataRequired()]) 

@app.route('/') #当地址是根路径时，就调用下面的函数
def index():
    # automatically checks whether a user has provided valid input text or not
    form = HelloForm(request.form)
    return render_template('first_app.html', form=form)  #form是想要传到first_app.html模板的参数
    
@app.route('/hello', methods=['POST'])  #firs_app.html中<form method=post action="/hello">互相关联
def hello():
    #render an HTML page hello.html after validating the HTML form
    form = HelloForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['sayhello']
        return render_template('hello.html', name=name)  #hello.html中的body相关联
    return render_template('first_app.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)    # activated Flask's debugger

    #对于 Web 应用，与客户端发送给服务器的数据交互至关重要。
    #  Flask 中由全局的 request 对象来提供这些信息

    #methods=['POST'] 是http的请求方法， POST请求会 向指定资源提交数据，
    # 请求服务器进行处理，如：表单数据提交、文件上传等，请求数据会被包含在请求体中