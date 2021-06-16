#!usr/bin/env python
#encoding:utf-8
from __future__ import division


'''
功能： 人脸识别摄像头视频流数据实时检测模块
'''


import cv2
from face_backserver.train_cnn_model import Model
from face_backserver.read_file import read_name_list
threshold=0.9  #辨认阈值



class Camera_reader(object):
    def __init__(self):
        self.model=Model()
        self.model.load()
        self.img_size=224


    # def build_camera(self):
    #     '''
    #     调用摄像头来实时人脸识别(人脸截取)
    #     '''
    #     face_cascade = cv2.CascadeClassifier('config/haarcascade_frontalface_alt.xml')
    #     # name_list = read_name_list('dataset')
    #     name_list = read_name_list('CASIA_3')
    #     cameraCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #     success, frame = cameraCapture.read()
    #     while success and cv2.waitKey(1) == -1:
    #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #         faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #         for (x,y,w,h) in faces:
    #             f = cv2.resize(gray[y:(y+h+30),x:(x+w)],(200,200))
    #             ROI = cv2.resize(f, (128,128),interpolation=cv2.INTER_AREA)
    #             label, prob = self.model.predict(ROI)
    #             print(prob)
    #             if prob >= threshold:
    #                 show_name = name_list[label]
    #             else:
    #                 show_name = "unknow"
    #             cv2.putText(frame, show_name, (x,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,255,2)
    #             frame = cv2.rectangle(frame,(x,y), (x+w,y+h),(255,0,0),2)
    #         cv2.imshow("Camera", frame)
    #         # yield show_name
    #     cameraCapture.release()
    #     cv2.destroyAllWindows()

    def online_camera(self,img,face_cascade,name_list):
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        for (x, y, w, h) in faces:
            f = cv2.resize(img[y:(y + h), x:(x + w)], (300, 300))
            ROI = cv2.resize(f, (224, 224), interpolation=cv2.INTER_AREA)
            label, prob = self.model.predict(ROI)
            show_name = name_list[label]
            print("概率:"+str(prob),"id:"+str(label),"名字"+show_name)
            if prob >= threshold:
                return label
            else:
                return None


    # def build_camera_2(self):
    #     '''
    #     调用摄像头来实时人脸识别(无人脸截取)
    #     '''
    #     face_cascade = cv2.CascadeClassifier('config/haarcascade_frontalface_alt.xml')
    #     name_list = read_name_list('dataset')
    #     cameraCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #     success, frame=cameraCapture.read()
    #     while success and cv2.waitKey(1) == -1:
    #         success,frame = cameraCapture.read()
    #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #         ROI=cv2.resize(gray, (self.img_size, self.img_size),interpolation=cv2.INTER_AREA)
    #         label, prob = self.model.predict(ROI)
    #         print(prob,name_list[label])
    #         if prob >= threshold:
    #             show_name = name_list[label]
    #         else:
    #             show_name="unknow"
    #
    #         faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #         for (x, y, w, h) in faces:
    #             cv2.putText(frame, show_name, (x,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,255,2)
    #             frame=cv2.rectangle(frame,(x,y), (x+w,y+h),(255,0,0),2)
    #         cv2.imshow("Camera", frame)
    #     cameraCapture.release()
    #     cv2.destroyAllWindows()
    #
    #
    # def build_picture(self):
    #     face_cascade = cv2.CascadeClassifier('config/haarcascade_frontalface_alt.xml')
    #     name_list = read_name_list('CASIA_1')
    #     print(name_list)
    #     frame = cv2.imread('CASIA_0/042/042_0.bmp')
    #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #     for (x, y, w, h) in faces:
    #         ROI = gray[x:x + w, y:y + h]
    #         ROI = cv2.resize(ROI, (self.img_size, self.img_size), interpolation=cv2.INTER_AREA)
    #         label, prob = self.model.predict(ROI)
    #         if prob >= threshold:
    #             show_name = name_list[label]
    #         else:
    #             show_name = "unknow"
    #         cv2.putText(frame, show_name+prob, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
    #         frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #         cv2.imwrite("result.jpg", frame)


if __name__ == '__main__':
    camera=Camera_reader()
    # camera.build_picture()