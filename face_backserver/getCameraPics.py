
 

'''
功能： Python  opencv调用摄像头获取个人图片
使用方法：
        启动摄像头后需要借助键盘输入操作来完成图片的获取工作
        c(change): 生成存储目录
        p(photo): 执行截图
        q(quit): 退出拍摄
'''
 
 
import os
import cv2
from face_backserver.read_file import read_list,readAllImg
import random
import numpy as np


#python2运行时加上d
# reload(sys)
# sys.setdefaultencoding('utf-8')


def cameraAutoForPictures(saveDir='data/'):
    '''
    调用电脑摄像头来自动获取图片
    '''
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    count = 1
    cap = cv2.VideoCapture(0)
    width, height, w = 640, 480, 360
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    crop_w_start = (width - w) // 2
    crop_h_start = (height - w) // 2
    print('width: ', width)
    print('height: ', height)
    while True:
        ret, frame = cap.read()
        frame = frame[crop_h_start:crop_h_start + w, crop_w_start:crop_w_start + w]
        frame = cv2.flip(frame, 1, dst=None)
        cv2.imshow("capture", frame)
        action = cv2.waitKey(1) & 0xFF
        if action == ord('c'):
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)
        elif action == ord('p'):
            cv2.imwrite("%s/%d.jpg" % (saveDir, count), cv2.resize(frame, (300, 300), interpolation=cv2.INTER_AREA))
            print(u"%s: %d 张图片" % (saveDir, count))
            count += 1
            if count == 500:
                break
        if action == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def readAllImg(path,*suffix):
    '''
    基于后缀读取文件
    '''
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
        print("读取成功")
        return resultArray


def endwith(s,*endstring):
    '''
    对字符串的后续和标签进行匹配
    '''
    resultArray = map(s.endswith,endstring)
    if True in resultArray:
        return True
    else:
        return False




def readPicSaveFace(sourcePath,objectPath,*suffix):
    '''
    图片标准化与存储
    '''
    if not os.path.exists(objectPath):
        os.makedirs(objectPath)
    try:
        resultArray=readAllImg(sourcePath,*suffix)
        count=1
        face_cascade=cv2.CascadeClassifier('config/haarcascade_frontalface_alt.xml')
        for i in resultArray:
            if type(i)!=str:
              faces=face_cascade.detectMultiScale(i, 1.3, 5)
              for (x,y,w,h) in faces:
                f=cv2.resize(i[y:(y+h),x:(x+w)],(300,300))
                cv2.imwrite(objectPath +"%d.jpg" % count, f)
                print(objectPath+"%d.jpg" % count)
                count+=1
        if count <5:
            print("============================"+count+"================")
    except Exception as e:
        print("Exception: ",e)
    else:
        print('Read  '+str(count-1)+' Faces to Destination '+objectPath)


#读取文件下的所有子文件夹识别人脸及灰度化，仅限于2层
def read_all_file(file_path,to_file_path):
    img_list,to_img_list=read_list(file_path,to_file_path)
    for i in range(len(img_list)):
        readPicSaveFace(img_list[i],to_img_list[i],'.jpg', '.JPG', 'png', 'PNG', 'tiff','bmp')

def img_brightness(image):
    contrast = np.random.randint(1,10)  # 对比度
    brightness = np.random.randint(50,100)  # 亮度
    pic_turn = cv2.addWeighted(image, contrast, image, 0, brightness).copy()
    return pic_turn

def img_translation(child_path,dir_image,image):
    # 图像平移 下、上、右、左平移
    M = np.float32([[1, 0, 0], [0, 1, 100]])
    img_down = cv2.warpAffine(image, M, (image.shape[1], image.shape[0])).copy()
    cv2.imwrite(child_path + '\\' + 'img_down_%s' % dir_image, img_down)

    M = np.float32([[1, 0, 0], [0, 1, -100]])
    img_up = cv2.warpAffine(image, M, (image.shape[1], image.shape[0])).copy()
    cv2.imwrite(child_path + '\\' + 'img_up_%s' % dir_image, img_up)

    M = np.float32([[1, 0, 100], [0, 1, 0]])
    img_right = cv2.warpAffine(image, M, (image.shape[1], image.shape[0])).copy()
    cv2.imwrite(child_path + '\\' + 'img_right_%s' % dir_image, img_right)

    M = np.float32([[1, 0, -100], [0, 1, 0]])
    img_left = cv2.warpAffine(image, M, (image.shape[1], image.shape[0])).copy()
    cv2.imwrite(child_path + '\\' + 'img_left_%s' % dir_image, img_left)

def convert_img1(img,alpha,beta):#亮度转换
    blank=np.zeros(img.shape,img.dtype)
    return cv2.addWeighted(img,alpha,blank,0,beta).copy()

def salt_and_pepper_noise(img,percentage):#椒盐噪声
    rows,cols = img.shape[0],img.shape[1]
    num = int(percentage*rows*cols)
    for i in range(num):
        x = random.randint(0,rows-1)
        y = random.randint(0, cols - 1)
        if random.randint(0,1)==0:
            img[x,y] = 0
        else:
            img[x,y] = 255
    return img

def gaussian_noise(img):#高斯随机噪声
    row, col, ch = img.shape
    mean = 0
    var = 0.1
    sigma = var ** 0.5
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    noisy = img + gauss
    return noisy

def improve_img(file_path):#数据增强
    for child_dir in os.listdir(file_path):
        child_path = os.path.join(file_path, child_dir)  # 得到path文件夹啊中的子文件路径
        for dir_image in os.listdir(child_path):
            if endwith(dir_image,'jpg'):  # 找到以jpg结尾的文件路径
                str = os.path.join(child_path,dir_image)
                img = cv2.imread(str)
                print(str)
                h_flip = cv2.flip(img, 1).copy()
                cv2.imwrite(child_path +'\\'+'h_flip_%s'% dir_image, h_flip)
                cv2.imwrite(child_path + '\\' + 'converted_lena1_%s' % dir_image, convert_img1(img.copy(),1.5,2))
                cv2.imwrite(child_path + '\\' + 'converted_lena2_%s' % dir_image, convert_img1(img.copy(),0.5,2))
                cv2.imwrite(child_path + '\\' + 'converted_lena3_%s' % dir_image, convert_img1(img.copy(), 1.25, 1))
                cv2.imwrite(child_path + '\\' + 'converted_lena4_%s' % dir_image, convert_img1(img.copy(), 0.25, 1))
                cv2.imwrite(child_path + '\\' + 'salt_and_pepper_noise1_%s' % dir_image, salt_and_pepper_noise(img.copy(),0.3))
                cv2.imwrite(child_path + '\\' + 'salt_and_pepper_noise2_%s' % dir_image,salt_and_pepper_noise(img.copy(), 0.1))
                cv2.imwrite(child_path + '\\' + 'gaussian_noise_%s' % dir_image, gaussian_noise(img.copy()))
                # img_translation(child_path,dir_image,img)
                # rows, cols, _ = img.shape
                # for x in (np.random.randint(-60,60,size=1)):# 旋转
                #     image_rotated = rotate_image(img,x, False)
                #     cv2.imwrite(child_path +'\\'+'image_rotated_%d_%s'% (x,dir_image),image_rotated)


def rotate_image(img, angle, crop):# 旋转
    crop_image = lambda img, x0, y0, w, h: img[y0:y0 + h, x0:x0 + w]  # 定义裁切函数，后续裁切黑边使用
    """
    angle: 旋转的角度
    crop: 是否需要进行裁剪，布尔向量
    """
    w, h = img.shape[:2]
    # 旋转角度的周期是360°
    angle %= 360
    # 计算仿射变换矩阵
    M_rotation = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    # 得到旋转后的图像
    img_rotated = cv2.warpAffine(img, M_rotation, (w, h),borderValue=(0,0,0)).copy()#(90,90,90)

    # 如果需要去除黑边
    if crop:
        # 裁剪角度的等效周期是180°
        angle_crop = angle % 180
        if angle > 90:
            angle_crop = 180 - angle_crop
        # 转化角度为弧度
        theta = angle_crop * np.pi / 180
        # 计算高宽比
        hw_ratio = float(h) / float(w)
        # 计算裁剪边长系数的分子项
        tan_theta = np.tan(theta)
        numerator = np.cos(theta) + np.sin(theta) * np.tan(theta)

        # 计算分母中和高宽比相关的项
        r = hw_ratio if h > w else 1 / hw_ratio
        # 计算分母项
        denominator = r * tan_theta + 1
        # 最终的边长系数
        crop_mult = numerator / denominator

        # 得到裁剪区域
        w_crop = int(crop_mult * w)
        h_crop = int(crop_mult * h)
        x0 = int((w - w_crop) / 2)
        y0 = int((h - h_crop) / 2)
        img_rotated = crop_image(img_rotated, x0, y0, w_crop, h_crop)
    return img_rotated

if __name__ == '__main__':
    # xxx替换为自己的名字
    # cameraAutoForPictures(saveDir='data_6/WG/')
    # readPicSaveFace('data/YX/', 'dataset1/YX/', '.jpg', '.JPG', 'png', 'PNG', 'tiff')
    # read_all_file('CASIA_0', 'data_RBG_new')
    improve_img('data_RBG_new')
    # improve_img('C:/Users/Hermit/Desktop/Facerecognition/program/1')
    # imgaug_improve_img('C:/Users/Hermit/Desktop/Facerecognition/program/ex_data/8.jpg')
    # readPicSaveFace('CASIA_0/000', 'CASIA_1/000', '.jpg', '.JPG', 'png', 'PNG', 'tiff','bmp')
    # readPicSaveFace('readPicSaveFace('data/YX/', 'dataset1/YX/', '.jpg', '.JPG', 'png', 'PNG', 'tiff')data/ludahui/', 'dataset1/ludahui/', '.jpg', '.JPG', 'png', 'PNG', 'tiff')
    # readPicSaveFace('data/lujunzhe/', 'dataset1/lujunzhe/', '.jpg', '.JPG', 'png', 'PNG', 'tiff')
    # readPicSaveFace('data/maweiguang/', 'dataset1/maweiguang/', '.jpg', '.JPG', 'png', 'PNG', 'tiff')
    # readPicSaveFace('data/menghu/', 'dataset1/menghu/', '.jpg', '.JPG', 'png', 'PNG', 'tiff')
    # readPicSaveFace('data/mengyu/', 'dataset1/mengyu/', '.jpg', '.JPG', 'png', 'PNG', 'tiff')
    # readPicSaveFace('data/wangxi/', 'dataset1/wangxi/', '.jpg', '.JPG', 'png', 'PNG', 'tiff')
    # readPicSaveFace('data/xujunfeng/', 'dataset1/xujunfeng/', '.jpg', '.JPG', 'png', 'PNG', 'tiff')
    # readPicSaveFace('data/yangchangdong/', 'dataset1/yangchangdong/', '.jpg', '.JPG', 'png', 'PNG', 'tiff')
    # readPicSaveFace('data/yuzhichao/', 'dataset1/yuzhichao/', '.jpg', '.JPG', 'png', 'PNG', 'tiff')
    # readPicSaveFace('data/xuxinpeng/', 'dataset1/xuxinpeng/', '.jpg', '.JPG', 'png', 'PNG', 'tiff')