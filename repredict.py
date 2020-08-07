#重新加载训练结果并做预测
import os
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from keras.utils.generic_utils import CustomObjectScope
from keras.applications.mobilenet import relu6, DepthwiseConv2D, preprocess_input


def repredict(filename):
    with CustomObjectScope({'relu6': relu6,'DepthwiseConv2D': DepthwiseConv2D}):
        model = load_model("./static/cats_dog_mobileNet.h5") #用新模型的权重，同一张图片的预测概率反而下降了，有必要对两个不同的权重进行测试集测试
    #print(model.summary())
    #加载单个图片用于预测
    #img_path = os.path.join('./static/images', filename) #cat为0，dog为1
    img_path = './static/images' + filename   #???????????改成这样会不会影响使用？
    #print(img_path)
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0) #channel first
    x = preprocess_input(x)
    #predict
    preds = model.predict(x)
    if 0 < preds < 0.5:
        print("目标预测为猫，概率为{}%".format((1-preds)*100))
        return ("Cat", (1-preds)*100)
    else:
        print("目标预测为狗，概率为{}%".format((preds)*100))
        return ("Dog", preds*100)


if __name__ == "__main__":
    """用于测试"""
    repredict('/Dog/dog.2001.jpg')