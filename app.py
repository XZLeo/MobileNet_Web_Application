import os
from flask import Flask, render_template, request, flash, make_response, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from shutil import move
from shutil import Error as SError
from threading import Thread

from repredict import repredict
from TryMobile import abc

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

#允许上传type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', "PNG", "JPG", 'JPEG']) #大写的.JPG是不允许的

#check type
def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1] in ALLOWED_EXTENSIONS 
    # 圆括号中的1是分割次数

#upload path
UPLOAD_FOLDER = './uploads'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """"目前只支持上传英文名"""
    if request.method == 'POST':
        #获取上传文件
        file = request.files['file']
        print(dir(file))
        #检查文件对象是否存在且合法
        if file and allowed_file(file.filename): #哪里规定file都有什么属性
            filename = secure_filename(file.filename) #把汉字文件名抹掉了，所以下面多一道检查
            if filename != file.filename:
               flash("only support ASCII name")
               return render_template('upload.html')            
            #save
            try:
                file.save(os.path.join(UPLOAD_FOLDER, filename)) #现在似乎不会出现重复上传同名文件的问题
            except FileNotFoundError:
                os.mkdir(UPLOAD_FOLDER)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('update', fileName=filename))
        else:
            return 'Upload Failed'
    else: #GET方法
        return render_template('upload.html')

def render_photo_as_page(filename):
    """每次调用都将上传的图片复制到static中"""
    img = Image.open(os.path.join(UPLOAD_FOLDER, filename))  #上传文件夹和static分离
    img.save(os.path.join('./static/images', filename)) #这里要求jpg还是png都必须保存成png，因为html里是写死的
    #predict
    preds = repredict(filename)
    result = {}
    result["prediction"] = preds[0]
    result["probability"] = preds[1]
    result["fileName"] =  filename
    return result     

@app.route('/upload/<path:fileName>', methods=['POST', 'GET'])
def update(fileName):
    """输入url加载图片，并返回预测值；上传图片，也会重定向到这里"""
    result = render_photo_as_page(fileName) 
    return render_template('show.html', fname='images/'+fileName, result=result)

@app.route('/thanks', methods=['POST', 'GET'])
def thanks():
    """怎么把上个页面显示的预测种类，返回到这个函数中"""
    category = request.form["Correctness"] #True or False
    prediction = request.form['prediction']
    fileName = request.form['filename']
    print(category, prediction, fileName)
    x = {"Cat", "Dog"}
    if category == 'Incorrect':
       prediction_set  = x - {prediction} #猫变狗，狗变猫
       prediction = prediction_set.pop()
    src = './static/{}'.format(fileName)
    dst = './static/images/{}'.format(prediction)
    print(src, dst)
    try:
        os.mkdir(dst)
    except FileExistsError:
        pass
    try:
        move(src, dst) #上传同名照片会报错
    except SError:
        flash("File arealdy exists or has the same name")
    #调用update去更新模型
    Thread(target=abc, args=()).start()  #这里没写完
    return render_template('thanks.html')


if __name__ == '__main__':
    app.run(debug=True)

#用secure_filename获取中文文件名时,中文会被省略。
#原因：secure_filename()函数只返回ASCII字符，非ASCII字符会被过滤掉

#flash是要在上传页面配合模板的get_flash使用的

#flask要求视图函数必须返回字符串或者模板

#redirect不能传值，但url_for可以传值



