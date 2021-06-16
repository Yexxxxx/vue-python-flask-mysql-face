import cv2
import os
import face_backserver.mysql_connect as mysql
def detectFaceOpenCVDnn(net, frame):
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    conf_threshold = 0.7
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
    return bboxes

def CatchPICFromVideo(window_name,camera_idx,img_path):
    num = 0
    #检查输入路径是否存在——不存在就创建
    cv2.namedWindow(window_name,)
    modelFile = "E:/code_collection/venv/opencv_face_detector_uint8.pb"
    configFile = "E:/code_collection/venv/opencv_face_detector.pbtxt"
    net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
    # 输入图片
    cap = cv2.VideoCapture(camera_idx, cv2.CAP_DSHOW)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    while cap.isOpened():
        ok, img = cap.read()  # 读取一帧数据
        if not ok:
            break
        if num >= 500:  # 如果超过指定最大保存数量退出循环
            break
        bboxes = detectFaceOpenCVDnn(net, img)
        for i in bboxes:
            img = cv2.rectangle(img, (i[0], i[1]), (i[2], i[3]), (171, 207, 49), 4)
        width = i[2]-i[0]
        high = i[3]-i[1]
        if ((i[2]-i[0]>200 and i[2]-i[0]<240) and (i[3]-i[1]>270 and i[3]-i[1]<340)):#i[2]-i[0]为宽，i[3]-i[1]为高
            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            image=grey[i[1]+5:i[3]-5,i[0]+5:i[2]-5]
            cv2.imwrite(img_path+'%d.jpg' % (num),image)
            cv2.putText(img, 'num:%d' % (num), (i[0] + 30, i[1] + 30), font, 1, (255, 0, 255),4)
            num += 1
        elif(width < 200 and high < 270):
            cv2.putText(img, " draw closer",(i[0]-20, i[1]-30), font, 1, (255, 0, 255),4)
        elif (width > 240 and high > 340):
            cv2.putText(img, "pull away",(i[0]-20, i[1]-30), font, 1, (255, 0, 255),4)
        else:
            cv2.putText(img, "Please look squarely",(i[0]-70, i[1]-30), font, 1, (255, 0, 255),4)
        cv2.imshow(window_name, img)
        c = cv2.waitKey(5)
        if c & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    PATH = 'dataset1/YX/'
    CatchPICFromVideo("1",0,PATH)