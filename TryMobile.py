from keras.applications.mobilenet import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input, decode_predictions
from keras.layers import Dense, GloabalAveragePooling2D
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import time

#迁移训练模型
base_model = MobileNet(input_shape=(224, 224, 3),weights='imagenet', include_top=False) #channel_last
# print(base_model.summary())
#没有top是去掉了最后的GAP层和Softmax层
x = base_model.output
x = GloabalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
#添加类别分类器，只有两类
classifier = Dense(1, activation='sigmoid')(x)
model = Model(inputs=base_model.input, outputs=classifier)

for layer in base_model.layers:
    layer.trainable=Flase

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc']) 

#文件路径
import os, shutil
original_dataset_dir = 'C:/Users/13718/.keras/datasets/dogs-vs-cats/train'
base_dir = 'C:/Users/13718/.keras/datasets/cats_and_dogs_small' # save small dataset

try:
    os.mkdir(base_dir)
except FileExistsError:
    print('FileExistsError1') #保证正常运行

train_dir = os.path.join(base_dir, 'train')
try:
    os.mkdir(train_dir)
except FileExistsError:
    print('FileExistsError2')
    
validation_dir = os.path.join(base_dir, 'validation')
try:
    os.mkdir(validation_dir)
except FileExistsError:
    print('FileExistsError3')

test_dir = os.path.join(base_dir, 'test')
try:
    os.mkdir(test_dir)
except FileExistsError:
    print('FileExistsError4')


#使用生成器读取图像
train_datagen = ImageDataGenerator(rescale=1./255) #所有像素缩小255倍
test_datagen = ImageDataGenerator(rescale=1./255) 

train_generator = train_datagen.flow_from_directory(
    train_dir,               #不同分类对应不同子目录
    target_size=(150, 150), 
    batch_size=20,
    class_mode='binary') #使用二进制标签

validation_generator = test_datagen.flow_from_directory(
    validation_dir,               
    target_size=(150, 150),  # 将图像调整为150*150
    batch_size=20,
    class_mode='binary') 


#加载单个图片用于预测
img_path = 'C:\\Users\\13718\\.keras\\datasets\\dogs-vs-cats\\train\\dog.3901.jpg'
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

preds = model.predict(x)
print('Predicted:', decode_predictions(preds, top=3)[0])
# 概率最大的三个预测



