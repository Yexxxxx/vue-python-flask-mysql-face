
import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
#读取所有图片
def readAllImg(path,*suffix):
    try:
        s = os.listdir(path)
        resultArray = []
        fileName = os.path.basename(path)
        resultArray.append(fileName)
        for i in s:
            if endwith(i, suffix):
                document = os.path.join(path, i)
                img = cv2.imread(document)
                resultArray.append(img)
    except IOError:
        print("Error")
    else:
        print ("读取成功")
        return resultArray

def Read_Folder():
    """
    读取文件夹下所有文件
    """
    FolderPath = "CASIA_3"
    files = os.listdir(FolderPath)
    files.sort(key=lambda fn: os.path.getmtime(FolderPath+'/'+fn))
    img_list = []
    label_list = []
    dir_counter = 0  # 记录文件夹的数量
    IMG_SIZE = 128
    # 对路径下的所有子文件夹中的所有jpg文件进行读取并存入到一个list中
    for child_dir in files:
        child_path = os.path.join(FolderPath, child_dir)  # 得到path文件夹啊中的子文件路径
        print(child_dir,child_path)
        for dir_image in os.listdir(child_path):
            if endwith(dir_image, 'jpg'):  # 找到以jpg结尾的文件路径
                str = os.path.join(child_path, dir_image)  # 具体的图片文件的路径
                print(str)
                img = cv2.imread(str)
                # print(type(img))
                resized_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_CUBIC)
                recolored_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
                img_list.append(recolored_img)
                label_list.append(dir_counter)
        dir_counter += 1

    # 返回的img_list转成了 np.array的格式
    img_list = np.array(img_list)

    # return img_list, label_list, dir_counter

#输入一个字符串一个标签，对这个字符串的后续和标签进行匹配
def endwith(s: object, endstring: object) -> object:
   resultArray = map(s.endswith,endstring)
   if True in resultArray:
       return True
   else:
       return False

def read_file(path):
    FolderPath = path
    files = os.listdir(FolderPath)
    files.sort(key=lambda fn: os.path.getmtime(FolderPath + '/' + fn))
    img_list = []
    label_list = []
    dir_counter = 0  # 记录文件夹的数量
    IMG_SIZE = 224
    # 对路径下的所有子文件夹中的所有jpg文件进行读取并存入到一个list中
    for child_dir in files:
        child_path = os.path.join(FolderPath, child_dir)  # 得到path文件夹啊中的子文件路径
        print(child_dir, child_path)
        for dir_image in os.listdir(child_path):
            if endwith(dir_image, 'jpg'):  # 找到以jpg结尾的文件路径
                str = os.path.join(child_path, dir_image)  # 具体的图片文件的路径
                img = cv2.imread(str)
                # print(type(img))
                resized_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_CUBIC)
                # recolored_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
                img_list.append(resized_img)
                label_list.append(dir_counter)
        dir_counter += 1

    # 返回的img_list转成了 np.array的格式
    img_list = np.array(img_list)

    return img_list,label_list,dir_counter

#读取训练数据集的文件夹，把他们的名字返回给一个list
def read_name_list(path):
    name_list = []
    files = os.listdir(path)
    files.sort(key=lambda fn: os.path.getmtime(path + '/' + fn))
    for child_dir in files:
        name_list.append(child_dir)
    return name_list

def read_list(path,to_path):
    name_list = []
    to_name_list=[]
    files = os.listdir(path)
    files.sort(key=lambda fn: os.path.getmtime(path + '/' + fn))
    for child_dir in files:
        child_path = os.path.join(path, child_dir+'\\')
        to_child_path = os.path.join(to_path,child_dir+'\\')
        name_list.append(child_path)
        to_name_list.append(to_child_path)
    return name_list,to_name_list

if __name__ == '__main__':
    read_list("CASIA_3","dataset")