from flask import Flask, render_template, request, jsonify,Response
import face_backserver.predict_user_face as predict
from flask_cors import cross_origin,CORS
import face_backserver.mysql_connect as mysql
import os
import time
import cv2
import numpy as np
import base64
from face_backserver.read_file import read_name_list
from flask_socketio import SocketIO, emit, join_room,leave_room, close_room, rooms, disconnect





app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'face'
CORS(app, supports_credentials=True)
face_cascade = cv2.CascadeClassifier('config/haarcascade_frontalface_alt.xml')
dataPath = '../face_backserver/data_RBG_new'
name_list = read_name_list(dataPath)
socketio = SocketIO(app, cors_allowed_origins="*")
print(name_list)

@app.route('/')
@app.route('/index',methods=['GET','POST'])#默认
def index():
    return "get in flask"

@app.route('/login',methods=['POST'])#登入
def user_login():
    flag = False
    data = request.json
    result = mysql.user_search(data['account'])
    if (result[0] == data['passwd']):
        flag = True
    return jsonify({'flag':flag,
                    'work_id':result[1]
                    })

@app.route('/register',methods=['POST'])#注册
def user_register():
    data = request.json
    print(data)
    result = mysql.user_insert(data['account'],data['passwd'],data['id'])
    return jsonify({'result':result})

@app.route('/loan_from',methods=['POST'])#借贷申请
def loan():
    data = request.json
    print(data)
    result = mysql.loan_insert(data['id'],data['monovalent'],data['work_id'],data['status'],data['time'])
    if result == "success":
        return jsonify({'result': "申请提交成功", 'type': result})
    else:
        return jsonify({'result': "申请提交失败", 'type': result})

@app.route('/table_massage',methods=['GET','POST'])#表单信息
def table():
    list = []
    result = mysql.face_all_info_search()
    # print(result)
    for one in result:
        list.append({'name': one[0],
                     'age': one[1],
                     'phone': one[2],
                     'sex': one[3],
                     'id': one[4],
                     'time': one[5],
                     'bank_number':one[7],
                     'identity':one[8],
                     })
    return jsonify({'result':list})

@app.route('/loan_massage',methods=['GET','POST'])#借贷信息
def loan_massage():
    list = []
    data = request.json
    result = mysql.loan_info_search(data["id"])
    for one in result:
        list.append({'monovalent': one[1],
                     'work_id': one[2],
                     'deathtime': one[3],
                     'statu': one[5],
                     })
    return jsonify({'result':list})

@app.route('/table_massage_del',methods=['POST'])#删除表某个信息
def massage_del():
    data = request.json
    result = mysql.face_info_del(data['id'])
    if result == "success":
        return jsonify({'result':"信息删除成功",'type':result})
    else:
        return jsonify({'result':"信息删除失败", 'type': result})

@app.route('/table_massage_edit',methods=['POST'])#编辑表某个信息
def massage_edit():
    data = request.json
    data = data['form']
    result = mysql.face_info_edi(data['name'], data['age'], data['phone'], data['sex'],data['id'])
    if result == "success":
        return jsonify({'result':"信息编辑成功",'type':result})
    else:
        return jsonify({'result':"信息编辑失败", 'type': result})

@app.route('/get_face' , methods=["POST"])#为新人脸信息录入
def newuser_information():
    if request.method == "POST":
        data = request.json
        img = base64.b64decode(data['imgData'])
        img = np.frombuffer(img, dtype='uint8')
        new_img_np = cv2.imdecode(img, cv2.IMREAD_COLOR)
        faces = face_cascade.detectMultiScale(new_img_np, 1.3, 5)
        result = False
        print(faces,len(faces),data)
        if len(faces) == 0:
            return jsonify({'result':"未捕捉到人脸，请重试",'type':'error'})
        else:
            for (x, y, w, h) in faces:
                img = cv2.resize(new_img_np[y:(y + h), x:(x + w)], (200, 200))
            Path = dataPath+'\\'+data['name']+"\\"
            if not os.path.exists(Path):
                os.makedirs(Path)
                result = mysql.insert_client(data['name'], data['age'], data['phone_number'], data['sex'],data['bank_number'],data['identity'], img)
            cv2.imwrite(Path+data['name']+time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+'.jpg', img)
            print(Path+data['name']+time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+'.jpg')
            if result == False:
                return jsonify({'result': "该客户已存在或数据库链接失败",'type':'error'})
    return jsonify({'result':"数据库与人脸图像写入成功",'type':'success'})



@app.route('/receiveImage', methods=["POST"])#通过人脸预测信息

def receive_image():
    if request.method == "POST":
        data = request.json
        img = base64.b64decode(data['imgData'])
        img = np.frombuffer(img, dtype='uint8')
        new_img_np = cv2.imdecode(img,cv2.IMREAD_COLOR)

        camera = predict.Camera_reader()
        id = camera.online_camera(new_img_np,face_cascade,name_list)
        if id == None or id == 'unknow':
            return jsonify({'result': 'null'})
        result = mysql.face_info_search(int(id)+1)
        print(result,)
        print(id, )
        print(id + 1,)
        if result == () or result == None:
            return jsonify({'result':'null'})
        result = result[0]
        return jsonify({'name': result[0],
                        'age': result[1],
                        'phone': result[2],
                        'id': result[4],
                        'sex': result[3],
                        'credit': result[6]
        })


#socketio
@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('test',namespace='api')
def test():
    print('触发test函数')

    socketio.emit('api', {'data': 'test_OK'}, namespace='api')
    # for i in range(1, 100):
    #     emit('recv',{'data':i})



if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True, host="127.0.0.1", port=5000)

