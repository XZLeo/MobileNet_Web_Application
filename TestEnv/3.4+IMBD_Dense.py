
# coding: utf-8

# # 电影评论——二分类问题

from keras.datasets import imdb
import numpy as np
old = np.load
np.load = lambda *a,**k: old(*a,**k,allow_pickle=True)
#上面三行是为了避免np版本和keras起冲突，重载了np。load

(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)
# keep the most commn 1w words



print(train_data[0]) #series of word index
print(train_labels[0]) # Positive or negative



print(max([max(sequence) for sequence in train_data])) #index<10000

word_index = imdb.get_word_index() #word→index
reverse_word_index = dict([(value, key) 
                           for (key, value) in word_index.items()]) #逆转键值对，建一个反过来的字典
decoded_review = ' '.join([reverse_word_index.get(i - 3, '?') 
                           for i in train_data[0][1:100]]) #最后写了train_data[0],j
print(decoded_review)


# ## 准备数据
# 使用onehot编码将每个train_data[i]转换成10000*原长度的编码

import numpy as np
def vectorize_sequence(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results
#训练数据、测试数据向量化
x_train = vectorize_sequence(train_data)
x_test = vectorize_sequence(test_data)

# 标签向量化
y_train = np.asarray(train_labels).astype('float32')
y_test = np.asarray(test_labels).astype('float32')


# ## 搭网络
# 带有relu激活的全连接层堆叠，适用于input向量output0-1的二分类问题
# 结构： 
# 1. 两个中间层，每层都有 16 个隐藏单元； 
# 2. 第三层输出一个标量，预测当前评论的情感。 
# 3. 中间层使用 relu 作为激活函数，最后一层使用 sigmoid 激活以输出一个 0~1 范围内的概率 值

from keras import models 
from keras import layers
model = models.Sequential()
model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid')) #第一个参数是units个数


# ## 选择Loss function和Optimizer
# 对于二分类问题，网络输出一个概率，适合使用二元交叉熵binary_crossentropy


model.compile(optimizer='rmsprop',
             loss = 'binary_crossentropy',
             metrics=['accuracy'])


# ## 配置优化器和使用自定义的损失和指标
# 
# metrics: 在训练和测试期间的模型评估标准。 通常你会使用 metrics = ['accuracy']。  
# 如果要为多输出模型的**不同输出**指定不同的评估标准， 还可以传递一个字典，如 metrics = {'output_a'：'accuracy'}。




from keras import optimizers
from keras import metrics

model.compile(optimizer=optimizers.RMSprop(lr=0.001), #这里的lr就是默认大小
             loss = 'binary_crossentropy',
             metrics=[metrics.binary_accuracy])


# 搭建验证集，**用于监视训练epoch的次数，调参用**  
# Note:验证集不是测试集


x_val = x_train[:10000]   #验证集
partial_x_train = x_train[10000:] #测试集

y_val = y_train[:10000]
partial_y_train = y_train[10000:]


# 训练模型
# batch_size 512 epoch20轮

histroy = model.fit(partial_x_train,
                   partial_y_train,
                   epochs=4,
                   batch_size=512,
                   validation_data=(x_val, y_val)) #训练同时显示测试集上的accuracy


# history的成员history是个字典，包含训练过程的数据

histroy_dict = histroy.history

# 使用Matplotlib绘制训练损失和验证损失等
import matplotlib.pyplot as plt
 
loss_values = histroy_dict['loss']
val_loss_values = histroy_dict['val_loss']

epochs = range(1, len(loss_values) + 1)

plt.plot(epochs, loss_values, 'bo', label='Training Loss') #bo蓝色圆点
plt.plot(epochs, val_loss_values, 'b', label='Validation Loss') #b蓝色实线
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.legend()

plt.show()

acc = histroy_dict['binary_accuracy']
val_acc = histroy_dict['val_binary_accuracy']

epochs = range(1, len(loss_values) + 1)

plt.plot(epochs, acc, 'bo', label='Training Accuracy') #bo蓝色圆点
plt.plot(epochs, val_acc, 'b', label='Validation Accuracy') #b蓝色实线
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.legend()

plt.show()


# 将20轮改为4轮再运行一遍  
# ## 测试结果
model.predict(x_test[1:10,]) #对测试集的前十个数据

# 这么看简单的情感分类似乎用DNN即可

# 后续实验证明4轮是最佳的  
# 改成32units 2层之后