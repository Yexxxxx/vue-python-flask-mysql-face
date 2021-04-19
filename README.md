# vue-python-flask-mysql-face
##### 该项目的主要目的是为了完成我的毕业设计，其中前端方面借鉴了一些GitHub上的项目加以改写。
## 开发主功能
以金融第三方机构为客户目标，目的功能为第三方金融机构在通过前端页面的交互中为其客户进行人脸识别以及新人脸录入的功能。
## 设计实现构成
前端方面的基础架构使用vue-cli脚手架+elementUI框架进行搭建。各个页面使用Vue-Router在整体进行配置实现跳转。视图页面通过调用封装组件构成。组件中通过emit或prop进行数据传输，对于全局传输数据使用Vuex。通过Axios进行后端的API使用。前端方面实现登入页面、注册页面、主页面的样式，详细包括表单提交、验证码、摄像头调用及拍照、侧边导航栏以及单页面布局。
后端方面使用python作为基础语言进行方法编写，封装后的方法由flask封装API提供前端调用。人脸识别部分的实现主要通过python的opencv库以及os库来对图片进行读取存储与预处理，使用keras库进行调用卷积神经网络的各个API接口进行搭建与模型训练。通过自学阅读keras库进行调参并使用matplotlib获得训练评估指标曲线。后端方面实现人脸录入与读取文件、模型训练、人脸预测结果返回、flask服务、数据库连接与增删查改
## 希望但未完成部分
首先是其中前端页面部分，现在是通过拍照来进行人脸提交识别的，但原先的预期是通过摄像头实时识别
其次里面的代码逻辑比较乱，因为没有什么时间来进行梳理
最后是模型问题，虽然模型的准确率比较高，但是有高概率会出现对于陌生人脸的高概率识别情况，这种情况初步怀疑是样本类太少，可以通过两个方法解决，一是直接扩大样本类，但是每一个样本类需要一定量的张量存储，这使得本就吃GPU的训练更难了。二是通过迁移学习，但这个我还不会。
## 近期秃头问题
导师让我加些金融元素.........我.......毫无头绪
