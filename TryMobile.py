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
    while True:
        for i in range(steps):
            print(i)
            batch_list = NewImgSet[0][i*batch_size: (i+1)*batch_size] #这里真的不会上溢？
            label_list = NewImgSet[1][i*batch_size: (i+1)*batch_size]
            img = [read_img(path, target_size, rescale) for path in batch_list] #每次只取1个batch
            #batch_img = np.concatenate([array for array in img]) #?？？？
            batch_img = np.array(img)
            yield batch_img, label_list            
    

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
        # 可以用flow_from_dataframe代替，传入path,但需要安装新的tf2.0
        # 原训练集猫狗各1000张，validation猫狗各500张
        update_gen = img_gen(ImgSet, BATCH_SIZE, TARGET_SIZE) #现在就是测试生成器对不对了
        #重新加载模型，设置可训练的部分,是不是应该只训练分类器？
        with CustomObjectScope({'relu6': relu6,'DepthwiseConv2D': DepthwiseConv2D}):
            model = load_model("./static/cats_dog_mobileNet.h5")
        #先冻结所有曾，再将倒数两层解冻 
        # 这里发现倒数第三层用了GAP，倒数第二层的dense其实没必要了，但我不想再训练了
        for layer in model.layers:
            layer.trainable = False
        model.layers[-1].trainable = True
        model.layers[-2].trainable = True
        
        model.compile(loss='binary_crossentropy',
                    optimizer='rmsprop', 
                    metrics=['acc'])
        model.fit_generator(update_gen, steps_per_epoch=5, epochs=5)
        #steps_per_epochs决定每轮生成器生成多少次？
        model.save('./static/cats_dog_mobileNet_ver1.h5') #会不会同名文件出错？
        #model.save('.\static\cats_dog_mobileNet_ver{}.h5'.format())
        #这里最好加入版本号，但是那样前面repredict也要改
    return
    
def Train():
    #迁移训练模型
    base_model = MobileNet(input_shape=(224, 224, 3),weights='imagenet', include_top=False) #channel_last
    for layer in base_model.layers:
        layer.trainable=False
    # print(base_model.summary())
    #没有top是去掉了最后的GAP层和Softmax层
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    #添加类别分类器，只有两类
    classifier = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=base_model.input, outputs=classifier)

    #文件路径   
    base_dir = 'C:/Users/13718/.keras/datasets/cats_and_dogs_small' # save small dataset
    train_dir = os.path.join(base_dir, 'train')
    validation_dir = os.path.join(base_dir, 'validation')
    
    #使用生成器读取图像
    train_datagen = ImageDataGenerator(rescale=1./255) #所有像素缩小255倍
    test_datagen = ImageDataGenerator(rescale=1./255) 

    train_generator = train_datagen.flow_from_directory(
        train_dir,               #不同分类对应不同子目录 
        #如果train_dir里面除了两个文件夹还有别的会怎么样？没影响
        # 即使cat和dog的数量不一样也不影响训练
        target_size=(224, 224), 
        batch_size=20,
        class_mode='binary') #使用二进制标签

    validation_generator = test_datagen.flow_from_directory(
        validation_dir,               
        target_size=(224, 224),  
        batch_size=20,
        class_mode='binary') 

    model.compile(loss='binary_crossentropy',
                optimizer='rmsprop', #手动设置学习率，默认的是
                metrics=['acc'])    

    begin = time()
    #重新训练分类器
    history = model.fit_generator(
            train_generator,
            steps_per_epoch=100,  #sample总数/batch_size
            epochs=5,
            validation_data=validation_generator,
            validation_steps=50)
    print("trainning time {}".format(time()-begin))
    # trainning time 2093.084360599518
    #训练完应保存权重
    model.save('.\static\cats_dog_mobileNet.h5')    
    #绘制训练结果
    #plotLossAcc(history)

#似乎必须用data_generator加载图片
if __name__ == "__main__":
    # reTrain()
    # 开始训练的cpu占用率达到100%
    # 8核cpu
    
    update()
    # 测试用
# import numpy as np
# np.save('./static/files_dog.npy', [])     
# np.save('./static/files_cat.npy', []) 
# exit()