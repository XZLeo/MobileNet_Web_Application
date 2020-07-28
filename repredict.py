#重新加载训练结果并做预测
import os
from keras.models import load_model
from keras.preprocessing import image
from keras.utils.generic_utils import CustomObjectScope
from keras.applications.mobilenet import relu6
from keras.applications.mobilenet import DepthwiseConv2D
import numpy as np
from keras.applications.mobilenet import preprocess_input, decode_predictions

with CustomObjectScope({'relu6': relu6,'DepthwiseConv2D': DepthwiseConv2D}):
    model = load_model("D:\\webAI\\cats_dog_mobileNet.h5")

print(model.summary())

#加载单个图片用于预测
img_path = 'C:\\Users\\13718\\Desktop\\mmexport1595488605310.jpg' #cat为0，dog为1
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

preds = model.predict(x)
if 0 < preds < 0.5:
    print("目标预测为猫，概率为{}%".format((1-preds)*100))
elif preds > 0.5:
    print("目标预测为狗，概率为{}%".format((preds)*100))
# # 概率最大的三个预测