from keras.applications.mobilenet import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input, decode_predictions
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
from plotAccLoss import plotLossAcc
from time import sleep, time
import os

BATCH_SIZE=20 #和下面保持一致

def abc():
    """sleep若干秒，完全是为了验证"""
    sleep(10)
    print("子线程结束")

def test():
    """新增文件更新训练"""
    old_files_cat = set(np.load('./static/files_cat.npy'))
    old_files_dog = set(np.load('./static/files_dog.npy'))

    path_cat = './static/images/Cat'
    path_dog = './static/images/Dog'

    files_cat = np.array(os.listdir(path_cat))
    files_dog = np.array(os.listdir(path_dog))
    np.save('./static/files_cat.npy', files_cat)
    np.save('./static/files_dog.npy', files_dog)

    new_cat = set(files_cat) - old_files_cat
    new_dog = set(files_dog) - old_files_dog



    #能否不用flow_dir解决
    # 这里似乎可以用flow_from_dataframe代替，传入文件名
    
    # #如果想要每次只训练新增的，还需要将文件按照写入时间排序，做记录。。太麻烦了
    # 鉴于这里的新增图片不会太大，就每次都用全部新增去训练
    # 原训练集猫狗各1000张，validation猫狗各500张
    # 按照访问时间排序，每次只取出访问时间>上次访问时间的
    # 收集到一个batch的图片在更新
    # 即使每次把所有新增都用了，也必须要外部txt存储上一次的文件最后访问时间


    


    
    


def reTrain():
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
   
    #original_dataset_dir = 'C:/Users/13718/.keras/datasets/dogs-vs-cats/train'
    base_dir = 'C:/Users/13718/.keras/datasets/cats_and_dogs_small' # save small dataset
    train_dir = os.path.join(base_dir, 'train')
    validation_dir = os.path.join(base_dir, 'validation')
    #test_dir = os.path.join(base_dir, 'test')

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
        target_size=(224, 224),  # 将图像调整为150*150
        batch_size=20,
        class_mode='binary') 

    model.compile(loss='binary_crossentropy',
                optimizer='rmsprop', #手动设置学习率，默认的是
                metrics=['acc'])    

    begin = time()
    #重新训练分类器
    history = model.fit_generator(
            train_generator,
            steps_per_epoch=100,
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
   test()