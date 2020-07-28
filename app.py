import os
from flask import Flask, render_template, request, flash, make_response
from werkzeug.utils import secure_filename
from PIL import Image
from repredict import repredict

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

# @app.route('/')
# def index():
#     return "Hello, User!"


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
        # print(file.filename)
        #检查文件对象是否存在且合法
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) #把汉字文件名抹掉了.....
            if filename != file.filename:
               flash("only support ASCII name")
               return render_template('upload.html')            
            #save
            try:
                file.save(os.path.join(UPLOAD_FOLDER, filename)) #现在似乎不会出现重复上传同名文件的问题
            except FileNotFoundError:
                os.mkdir(UPLOAD_FOLDER)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            return render_photo_as_page(filename)
        else:
            return 'Upload Failed'
    else: #GET方法
        return render_template('upload.html')

def render_photo_as_page(filename):
    """每次调用都重写static/images/test.png"""
    img = Image.open(os.path.join(UPLOAD_FOLDER, filename))  #上传文件夹和static分离
    img.save(os.path.join('./static/images', filename)) #这里要求jpg还是png都必须保存成png，因为html里是写死的
    preds = repredict(filename)
    return render_template('show.html', fname='images/'+filename, preds=preds)
    #flask要求视图函数必须返回字符串或者模板

if __name__ == '__main__':
    app.run(debug=True)

#用secure_filename获取中文文件名时,中文会被省略。
#原因：secure_filename()函数只返回ASCII字符，非ASCII字符会被过滤掉
#安装pypinyin包，将汉字文件名转换成拼音

#flash是要在上传页面配合模板的get_flash使用的



