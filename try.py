from keras.applications.mobilenet import MobileNet, relu6, DepthwiseConv2D
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model, load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.generic_utils import CustomObjectScope
import numpy as np
from plotAccLoss import plotLossAcc
from time import sleep, time
import os
from PIL import Image
import math

BATCH_SIZE = 20 #和下面保持一致
TARGET_SIZE = (224, 224)

def read_img(path, target_size, rescale):
    '''读取单张图片，返回channel_first的4d数组'''
    try:
        img = Image.open(path).convert("RGB")
        img_rs = img.resize(target_size)
    except Exception as e:
        print(e)
    else:
        #x = np.expand_dims(np.array(img_rs), axis=0) #0指定channel在前
        x = np.array(img_rs)
        print(x.shape) #(1, 224, 224, 3)
        return x * rescale

def img_gen(NewImgSet, batch_size, target_size, rescale=1./255):
    """NewImgSet是元组分别存new_Cat路径和new_Dog路径
    cat label is 0
    dog label is 1
    """
    #这里应该rescale把图片都缩放到0.x的大小
    length = NewImgSet.shape[1]
    steps = math.ceil(length/batch_size) #确定每轮多少个batch，向上取整
    print(length, steps)
    i = 0
    batch_list = NewImgSet[0][i*batch_size: (i+1)*batch_size] #这里真的不会上溢？
    label_list = NewImgSet[1][i*batch_size: (i+1)*batch_size]
    img = [read_img(path, target_size, rescale) for path in batch_list] #每次只取1个batch
    print(np.array(img).shape, img[0:1], '\n', '换行')
    batch_img = np.array(img)
    #batch_img = np.concatenate([array for array in img]) #?？？？
    print(batch_img.shape, batch_img[0:1])
    return batch_img, label_list         
    #打印结果看出img的形状是   (20, 1, 224, 224, 3) 
    # batch_img形状是(20, 224, 224, 3)
    

def update():
    """新增文件更新训练"""
    # 必须要外部.npy文件存储上一次的所有标签图片
    old_files_cat = set(np.load('./static/files_cat.npy'))
    old_files_dog = set(np.load('./static/files_dog.npy'))
    #print(old_files_cat)

    path_cat = './static/images/Cat/'
    path_dog = './static/images/Dog/'

    files_cat = np.array([path_cat+file
     for file in os.listdir(path_cat)])  #给每个file加上路径
    #print(files_cat)
    files_dog = np.array([path_dog+file
     for file in os.listdir(path_dog)])
    np.save('./static/files_cat.npy', files_cat)
    np.save('./static/files_dog.npy', files_dog)
    #每次新图片上传都没有编号，其实应该编号啊.......
    new_cat = list(set(files_cat) - old_files_cat) 
    #print(set(files_cat) - old_files_cat)
    new_dog = list(set(files_dog) - old_files_dog)
    
    #如果多于一个batch，才会更新
    if len(new_cat) + len(new_dog) >= BATCH_SIZE: 
        NSet = new_cat + new_dog
        label_cat = np.zeros(len(new_cat))
        label_dog = np.ones(len(new_dog))
        labels = np.concatenate((label_cat, label_dog)) #only one axis
        ImgSet = np.array([NSet, labels])  
        #print(ImgSet)
        
        # 可以用flow_from_dataframe代替，传入path,但需要安装新的tf2.0
        # 原训练集猫狗各1000张，validation猫狗各500张
        img_gen(ImgSet, BATCH_SIZE, TARGET_SIZE) #现在就是测试生成器对不对了
        #print(next(update_gen))
        # print(next(update_gen))
        # print(next(update_gen))    
    return

if __name__ == "__main__":
    # reTrain()
    # 开始训练的cpu占用率达到100%
    # 8核cpu
    
    update()

    #经过测试，read_img和data_gen里先加一个轴，再减一个轴的操作完全多余！！！