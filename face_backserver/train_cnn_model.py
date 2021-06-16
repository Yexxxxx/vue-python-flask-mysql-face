
from face_backserver.read_file import read_file
from keras.models import Sequential, load_model
import keras.models as models
from sklearn.model_selection import train_test_split
from keras.utils import np_utils,plot_model
import random
from keras.preprocessing.image import ImageDataGenerator,load_img,img_to_array,array_to_img
from keras.metrics import Precision,Recall,categorical_accuracy,top_k_categorical_accuracy
from keras.optimizers import SGD
import matplotlib.pyplot as plt
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten,Dropout,BatchNormalization
from keras import layers
from keras.applications import mobilenet,vgg16,vgg19,resnet,nasnet,mobilenet_v2,xception
import numpy as np
from keras.callbacks import EarlyStopping,ReduceLROnPlateau
import tensorflow as tf
from keras import backend as K
from numba import cuda
#建立一个用于存储和格式化读取训练数据的类
import os

class DataSet(object):
   def __init__(self,path):
       self.num_classes = None
       self.X_train = None
       self.X_test = None
       self.Y_train = None
       self.Y_test = None
       self.img_size = 224#128
       self.extract_data(path) #在这个类初始化的过程中读取path下的训练数据
       self.history= None
   def extract_data(self,path):
        #根据指定路径读取出图片、标签和类别数
        imgs,labels,counter = read_file(path)

        #将数据集打乱随机分组，测试数据占数据集的20%
        X_train,X_test,y_train,y_test = train_test_split(imgs,labels,test_size=0.3,random_state=random.randint(0, 100))
        print(X_train.shape)
        #重新格式化和标准化

        X_train = X_train.reshape(X_train.shape[0],  self.img_size, self.img_size,3)/255.
        X_test = X_test.reshape(X_test.shape[0], self.img_size, self.img_size, 3)/255.

        X_train = X_train.astype('float32')
        X_test = X_test.astype('float32')

        Y_train = np_utils.to_categorical(y_train, num_classes=counter)
        Y_test = np_utils.to_categorical(y_test, num_classes=counter)


        # 将labels转成 binary class matrices


        #将格式化后的数据赋值给类的属性上
        self.X_train = X_train
        self.X_test = X_test
        self.Y_train = Y_train
        self.Y_test = Y_test
        self.num_classes = counter

   def check(self):
       print('num of dim:', self.X_test.ndim)
       print('shape:', self.X_test.shape)
       print('size: hn', self.X_test.size)

       print('num of dim:', self.X_train.ndim)
       print('shape:', self.X_train.shape)
       print('size:', self.X_train.size)
# 建立一个基于CNN的人脸识别模型
class Model(object):
    FILE_PATH = "../face_backserver/face_model_RBG_new_mobilenet.h5"  # 模型进行存储和读取的地方
    IMAGE_SIZE = 224  # 模型接受的人脸图片一定得是128*128的

    def __init__(self):
        self.model = None

    # 读取实例化后的DataSet类作为进行训练的数据源
    def read_trainData(self, dataset):
        self.dataset = dataset

    # 建立一个CNN模型
    def build_model(self):

        base_model =mobilenet.MobileNet(input_shape=(224,224,3),alpha=1.0 ,include_top=False, weights='imagenet', input_tensor=None, pooling=None, classes=self.dataset.num_classes)

        # self.model = Sequential()
        # self.model.add(Convolution2D(filters=96,kernel_size=(7,7),strides=(4, 4),padding='valid',
        #                              data_format='channels_last',input_shape=self.dataset.X_train.shape[1:]))
        # # self.model.add(BatchNormalization())#标准化
        # self.model.add(Activation('relu'))#激活层
        # self.model.add(MaxPooling2D(pool_size=(3, 3),strides=(2, 2),padding='valid'))
        #
        # self.model.add(Convolution2D(filters=256, kernel_size=(5, 5), strides=(1, 1), padding='same'))
        # self.model.add(Activation('relu'))
        # self.model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same'))
        #
        # self.model.add(Convolution2D(filters=384, kernel_size=(3, 3), strides=(1, 1), padding='same'))
        # self.model.add(Activation('relu'))
        # self.model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same'))
        #
        # self.model.add(Convolution2D(filters=256, kernel_size=(3, 3), strides=(1, 1), padding='same'))
        # self.model.add(Activation('relu'))
        # self.model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='same'))



        top_model= Sequential()
        top_model.add(Convolution2D(filters=512, kernel_size=(3, 3), strides=(1, 1), padding='valid',input_shape=base_model.output_shape[1:]))
        # self.model.add(BatchNormalization())#标准化
        top_model.add(Activation('relu'))  # 激活层
        top_model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding='valid'))


        top_model.add(Flatten())
        top_model.add(Dense(4096))
        top_model.add(Activation('relu'))
        top_model.add(Dropout(0.3))
        top_model.add(Dense(4096))
        top_model.add(Activation('relu'))
        top_model.add(Dropout(0.3))
        top_model.add(Dense(self.dataset.num_classes))
        top_model.add(Activation('softmax'))
        self.model = models.Model(inputs=base_model.input, outputs=top_model(base_model.output))



        # self.model.add(Flatten())
        # self.model.add(Dense(4096))
        # self.model.add(Activation('relu'))
        # self.model.add(Dropout(0.3))
        # self.model.add(Dense(4096))
        # self.model.add(Activation('relu'))
        # self.model.add(Dropout(0.3))
        # self.model.add(Dense(self.dataset.num_classes))
        # self.model.add(Activation('softmax'))脸识别场景下的金融反欺诈模型脸识别场景下的金融反欺诈模型脸识别场景下的金融反欺诈模型


        self.model.summary()

    def train_model(self):

        sgd = SGD(lr=0.0001, decay=1e-6,
                  momentum=0.9, nesterov=True)
        early_stopping = EarlyStopping(monitor='val_loss', patience=12)
        for i, layer in enumerate(self.model.layers):
            print(i, layer.name)
        trainable_layer = 48
        for i in range(trainable_layer):
            self.model.layers[i].trainable = False
        reducelr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=8, verbose=1, mode='min')
        datagen = ImageDataGenerator(
            rotation_range=45,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.15,
            zoom_range=0.15,
            horizontal_flip=True,
            # rescale=1./255,
            # vertical_flip=True,
            fill_mode='nearest',
            )
        # datagen.fit(self.dataset.X_train)
        self.model.compile(
            # optimizer='adam',
            optimizer=sgd,
            loss='categorical_crossentropy',
            metrics=[categorical_accuracy,Precision(),Recall()])
        # epochs、batch_size为可调的参数，epochs为训练多少轮、batch_size为每次训练多少个样本
        self.history = self.model.fit(
            datagen.flow(self.dataset.X_train,self.dataset.Y_train,batch_size=6,shuffle=True),
            epochs=1000,
            verbose = 1,
            # validation_data=datagen.flow(self.dataset.X_train,self.dataset.Y_train,batch_size=1,subset="validation"),
            validation_data=(self.dataset.X_test, self.dataset.Y_test,),
            shuffle=True,
            callbacks=[early_stopping,reducelr])

        # self.history = self.model.fit(
        #     self.dataset.X_train,
        #     self.dataset.Y_train,
        #     batch_size=16,
        #     shuffle=True,
        #     epochs=1000,
        #     validation_split=0.3,
        #     callbacks=[early_stopping,reducelr])

    def evaluate_model(self):
        print('\nTesting---------------')

        loss,accuracy,precision, recall= self.model.evaluate(self.dataset.X_test, self.dataset.Y_test,verbose=1)
        print('\ntest loss;', loss)
        print('\ntest accuracy:', accuracy)
        print('\ntest precision:', precision)
        print('\ntest recall:', recall)



        plt.plot(self.history.history['loss'])
        plt.plot(self.history.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('rate')
        plt.xlabel('Epoch')
        plt.legend(['loss', 'val_loss'], loc='upper left')
        plt.show()

        plt.plot(self.history.history['categorical_accuracy'])
        plt.plot(self.history.history['val_categorical_accuracy'])
        plt.title('Model categorical_accuracy')
        plt.ylabel('rate')
        plt.xlabel('Epoch')
        plt.legend(['accuracy', 'val_categorical_accuracy'], loc='upper left')
        plt.show()

        plt.plot(self.history.history['val_categorical_accuracy'])
        plt.plot(self.history.history['val_loss'])
        plt.plot(self.history.history['val_precision'])
        plt.plot(self.history.history['val_recall'])
        plt.title('Model val_metrics')
        plt.ylabel('rate')
        plt.xlabel('Epoch')
        plt.legend(['val_accuracy', 'val_loss', 'val_precision', 'val_recall'], loc='upper left')
        plt.show()

    def save(self, file_path=FILE_PATH):
        self.model.save(file_path)
        #self.model.save_weights(file_path)
        print('Model Saved.')

    def load(self, file_path=FILE_PATH):
        self.model = load_model(file_path)
        print('Model Loaded.')

    # 需要确保输入的img得是灰化之后（channel =1 )且 大小为IMAGE_SIZE的人脸图片
    def predict(self, img):

        img = img.reshape(1,self.IMAGE_SIZE,self.IMAGE_SIZE,3)/255.0
        img = img.astype('float32')
        result = self.model.predict(img,batch_size = 32)  # 测算一下该img属于某个label的概率
        max_index = np.argmax(result)  # 找出概率最高的

        return max_index, result[0][max_index]  # 第一个参数为概率最高的label的index,第二个参数为对应概率

if __name__ == '__main__':
    dataset = DataSet('data_RBG_new')
    model = Model()
    # model.test('CASIA_1')
    model.read_trainData(dataset)
    model.build_model()
    model.train_model()
    model.save()
    model.evaluate_model()


