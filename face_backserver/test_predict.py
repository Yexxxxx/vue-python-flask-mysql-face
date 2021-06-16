import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from face_backserver.read_file import read_name_list,read_file,endwith
from face_backserver.train_cnn_model import Model
import cv2

#读取一张图片进行识别
def test_Pictures(path):
    model= Model()
    model.load()
    for child_dir in os.listdir(path):
        if endwith(child_dir, 'jpg'):  # 找到以jpg结尾的文件路径
            str = os.path.join(path, child_dir)  # 具体的图片文件的路径
            img = cv2.imread(str)
            resized_img = cv2.resize(img, (224, 224),interpolation=cv2.INTER_AREA)
            picType,prob = model.predict(resized_img)
            if picType != -1:
                name_list = read_name_list('data_RBG_new')
                print (child_dir,name_list[picType],prob)
            else:
                print (" Don't know this person")

def test_Pictures_2(path):
    model= Model()
    model.load()
    face_cascade = cv2.CascadeClassifier('config/haarcascade_frontalface_alt.xml')
    for child_dir in os.listdir(path):
        if endwith(child_dir, 'jpg'):  # 找到以jpg结尾的文件路径
            str = os.path.join(path, child_dir)  # 具体的图片文件的路径
            img = cv2.imread(str)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(img, 1.3, 5)
            for (x,y,w,h) in faces:
                f=cv2.resize(img[y:(y+h),x:(x+w)],(224, 224))
                resized_img = cv2.resize(f, (224, 224),interpolation=cv2.INTER_AREA)
                picType, prob = model.predict(resized_img)
                if picType != -1:
                    name_list = read_name_list('data_RBG_new')
                    print (child_dir,name_list[picType],picType,prob)
                else:
                    print (" Don't know this person")

#读取文件夹下子文件夹中所有图片进行识别
def test_onBatch(path):
    model= Model()
    model.load()
    index = 0
    img_list, label_lsit, counter = read_file(path)
    print(img_list)
    test_Pictures_2(img_list)
    return index

if __name__ == '__main__':
    #test_onePicture('pictures/test_photos/zhouyicheng/zhouyicheng_1.jpg')
    #test_onePicture('pictures/test_photos/zhouyicheng/zhouyicheng_2.jpg')
    #test_onePicture('pictures/test_photos/louxingyu/louxingyu_1.jpg')
    # test_Pictures('data/ludahui')
    # test_Pictures('pictures/take_photos')
    test_Pictures('test')
    print("--------------截取人脸--------------------")
    test_Pictures_2('test')
    # test_onBatch("CASIA_0")
    # test_Pictures_2('data/JRJNB')