import os
import numpy as np

from keras.models import load_model
from keras.preprocessing import image
from keras.utils.generic_utils import CustomObjectScope
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.mobilenet import relu6, DepthwiseConv2D, preprocess_input

with CustomObjectScope({'relu6': relu6,'DepthwiseConv2D': DepthwiseConv2D}):
        model = load_model("./static/cats_dog_mobileNet_ver1.h5")

base_dir = 'C:/Users/13718/.keras/datasets/cats_and_dogs_small'

test_dir = os.path.join(base_dir, 'test')

test_datagen = ImageDataGenerator(rescale=1./255) 

test_generator = test_datagen.flow_from_directory(
        test_dir,               
        target_size=(224, 224),  
        batch_size=20,
        class_mode='binary') 
print(next(test_generator)) #打印的结果和自定义的结果是差不多的
test_loss, test_acc = model.evaluate_generator(test_generator, steps=50) #样本数100z0/batch_size
print('test_loss:', test_loss, ' test_acc:', test_acc)

# test和validation是不需要rescale的
#本身在Imagenet上训练的分类精度就已经很高，这里单纯为了实现更新权重
# 并没有死循环，只是不打印进度条，时间还很长

# 使用原始h5 test_loss: 0.05041411317419261  test_acc: 0.9809999966621399
# 使用没有rescale的ver1.h5 test_loss: 0.12166374944150447  test_acc: 0.9789999961853028
# 使用带rescale的test_loss: 0.11561190240085124  test_acc: 0.980999995470047
