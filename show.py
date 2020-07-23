#用于展示MobileNet对分类进行预测
from keras.applications.mobilenet import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input, decode_predictions
from keras.models import Model
import numpy as np



model = MobileNet(weights='imagenet')

#加载单个图片用于预测
img_path = 'C:\\Users\\13718\\Desktop\\654cafaeee71e129db72a3a68885f75b_w.jpg'
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

preds = model.predict(x)
print('Predicted:', decode_predictions(preds, top=3)[0])
# 概率最大的三个预测
