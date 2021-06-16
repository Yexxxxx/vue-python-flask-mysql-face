<template>
    <div >
        <el-row :gutter="20">
            <el-col :span="8">
                <el-card shadow="hover" class="mgb20" style="height:252px;">
                    <div class="user-info">
                        <img src="../assets/test.png" class="user-avator" >
                        <div class="user-info-cont">
                            <div class="user-info-name">{{account}}</div>
                            <div>{{role}}</div>
                        </div>
                    </div>
                </el-card>
                <el-card  shadow="hover" style="height:252px;">
                    <div>
                        <el-button size="medium"  @click="handleCreate()">人脸录入</el-button>
                    </div>
                    <div style="margin-top: 20px">
                        <el-button size="medium" @click="image_cap()">人脸识别</el-button>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="16">
                <el-row :gutter="20" class="mgb20">
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-1">
                                <i class="el-icon-s-custom grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">0</div>
                                    <div>用户流量</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-2">
                                <i class="el-icon-bell grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">0</div>
                                    <div>消息通知</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{padding: '0px'}">
                            <div class="grid-content grid-con-3">
                                <i class="el-icon-coordinate grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">0</div>
                                    <div>合同流量</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
                <el-card shadow="hover" style="height:403px;">
                    <el-switch
                            v-model="value1"
                            active-text="开启摄像"
                            :disabled="isDisabled"
                            inactive-text="关闭摄像">
                    </el-switch>
                    <el-card shadow="hover">
                        <div class="grid-face ">
                            <video id="videoCamera" :width="videoWidth" :height="videoHeight" autoplay></video>
                            <canvas style="display:none;" id="canvasCamera" :width="videoWidth" :height="videoHeight" ></canvas>
                            <div class="grid-cont-right" style="font-size:24px;color: black">
                                <div >姓名：{{face.name}}</div>
                                <div>年龄：{{face.age}}</div>
                                <div>性别：{{face.sex}}</div>
                                <div>手机号：{{face.phone}}</div>
                                <div>身份证：{{face.id}}</div>
                            </div>
                        </div>
                    </el-card>
                </el-card>
            </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="12">
                <el-card shadow="hover" style="height:270px;">
                    <div style="padding: 15px;">
                        <el-form  :model="loan" label-width="70px"  method="post">
                            <el-form-item label="审批人" prop="work_id">
                                <el-input :disabled="true" size="medium" placeholder="审批人" v-model="account"></el-input>
                            </el-form-item>
                            <el-form-item label="借贷金额"  prop="monovalent">
                                <el-input v-model="loan.monovalent" oninput="value=value.replace(/[^\d]/g, '')"  size="medium" placeholder="借贷金额"  ></el-input>
                            </el-form-item>
                            <el-form-item label="还款时间"  prop="time">
                                <el-date-picker  v-model="loan.time" type="date"  @change="getTime" value-format="yyyy-MM-dd"  placeholder="还款时间" style="width: 100%;"></el-date-picker>
                            </el-form-item>
                            <el-button  type="primary"  size="medium" @click="put_loan">提交申请</el-button>
                        </el-form>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card shadow="hover" style="height:270px;">
                    <X_circle :credit="face.credit"></X_circle>
                </el-card>
            </el-col>
        </el-row>



        <el-dialog :visible.sync="dialogFormVisible" center width="400px">
            <el-form
                    :model="Form"
                    ref="dataForm"
                    :rules="rules"
                    label-position="left"
                    label-width="100px"
                    style="width: 300px;"
            >
                <el-form-item label="姓名" prop="name" >
                    <el-input v-model="Form.name" />
                </el-form-item>
                <el-form-item label="性别" prop="sex">
                    <el-radio-group v-model="Form.sex" style="margin-right:12px;">
                        <el-radio v-for="(radio, index) in subjectList" :key="index" :label="radio">{{radio}}</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="年龄"   prop="age">
                    <el-input v-model="Form.age" />
                </el-form-item>
                <el-form-item label="联系电话" prop="phone">
                    <el-input v-model="Form.phone" />
                </el-form-item>
                <el-form-item label="银行卡号" prop="phone">
                    <el-input v-model="Form.bank_number" />
                </el-form-item>
                <el-form-item label="身份证号" prop="phone">
                    <el-input v-model="Form.identity" />
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="get_face()">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import axios from 'axios';
    import X_circle from "../components/X_circle";
    export default {
        name: 'index',
        data() {
            return {
                videoWidth: 380,
                videoHeight: 400,
                value1: false,
                account: this.$store.state.account,
                isDisabled:false,
                flag:true,
                subjectList: ["男", "女"],
                dialogFormVisible: false,
                imgData:'',
                test:this.$store.state.work_id,
                Form: {
                    name: "",
                    sex: "",
                    age: "",
                    phone: "",
                    bank_number:'',
                    identity:'',

                },
                face: {
                    name: '未知',
                    age: '未知',
                    id:'未知',
                    phone:'未知',
                    sex:'未知',
                    credit:'',
                },
                rules: {
                    name: [
                        { required: true, message: '姓名不能为空', trigger: 'blur' },
                        { min: 2, max: 4, message: '长度在 2 到 4 个字符', trigger: 'blur' }
                    ],
                    sex: [
                        { required: true, message: '请选择性别', trigger: 'change' }
                    ],
                    age: [
                        { required: true, message: '年龄不能为空', trigger: 'blur' },
                    ],
                },
                loan:{
                    monovalent:'',
                    time:'',
                    status:'待审批',
                },
                disabledDate(time) {
                    return time.getTime() > Date.now()
                },
                shortcuts: [{
                    text: 'Today',
                    value: new Date(),
                }, {
                    text: 'Yesterday',
                    value: (() => {
                        const date = new Date()
                        date.setTime(date.getTime() - 3600 * 1000 * 24)
                        return date
                    })(),
                }, {
                    text: 'A week ago',
                    value: (() => {
                        const date = new Date()
                        date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
                        return date
                    })(),
                }],
            };
        },
        created(){

        },
        mounted(){

        },
        destroyed(){
            this.stopCompetence()
        },
        components: {
            X_circle
        },
        watch:{
            value1(val){
                if (val == true){
                    this.getCompetence()
                    this.timeout_click()
                }
                else {
                    this.stopCompetence()
                    this.timeout_click()
                }
            }
        },
        computed: {
            role() {
                return this.name === 'admin' ? '超级管理员' : '普通用户';
            },
        },

        methods: {
            getCompetence () {
                var _this = this
                this.thisCancas = document.getElementById('canvasCamera')
                this.thisContext = this.thisCancas.getContext('2d')
                this.thisVideo = document.getElementById('videoCamera')
                // 旧版本浏览器可能根本不支持mediaDevices，我们首先设置一个空对象

                if (navigator.mediaDevices === undefined) {
                    navigator.mediaDevices = {}
                }
                // 一些浏览器实现了部分mediaDevices，我们不能只分配一个对象
                // 使用getUserMedia，因为它会覆盖现有的属性。
                // 这里，如果缺少getUserMedia属性，就添加它。
                if (navigator.mediaDevices.getUserMedia === undefined) {
                    navigator.mediaDevices.getUserMedia = function (constraints) {
                        // 首先获取现存的getUserMedia(如果存在)
                        var getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.getUserMedia
                        // 有些浏览器不支持，会返回错误信息
                        // 保持接口一致
                        if (!getUserMedia) {
                            return Promise.reject(new Error('浏览器不支持'))
                        }
                        // 否则，使用Promise将调用包装到旧的navigator.getUserMedia
                        return new Promise(function (resolve, reject) {
                            getUserMedia.call(navigator, constraints, resolve, reject)
                        })
                    }
                }
                var constraints = { audio: false, video: { width: this.videoWidth, height: this.videoHeight, transform: 'scaleX(-1)' } }

                navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
                    // 旧的浏览器可能没有srcObject
                    if ('srcObject' in _this.thisVideo) {
                        _this.thisVideo.srcObject = stream
                    } else {
                        // 避免在新的浏览器中使用它，因为它正在被弃用。
                        _this.thisVideo.src = window.URL.createObjectURL(stream)
                    }

                    _this.thisVideo.onloadedmetadata = function (e) {
                        console.log(e)
                        _this.thisVideo.play()
                    }
                }).catch(err => {
                    console.log(err)
                })
            },

            stopCompetence() {
                this.thisVideo.srcObject.getTracks()[0].stop()
            },
            timeout_click(){
                this.isDisabled = true
                setTimeout(()=>{
                    this.isDisabled=false
                },3000)
            },

            get_face() {

                const url = 'http://127.0.0.1:5000/get_face';
                console.log(this.Form)
                axios({
                    method: 'post',
                    url:url ,
                    data:{
                        imgData:this.imgData,
                        name:this.Form.name,
                        sex:this.Form.sex,
                        age:this.Form.age,
                        phone_number:this.Form.phone,
                        bank_number:this.Form.bank_number,
                        identity:this.Form.identity,
                    }
                })
                    .then((res) => {
                        console.log(res.data);
                        this.dialogFormVisible = false
                        this.$message({
                            message:res.data.result,
                            type:res.data.type
                        });
                    })
            },

            // test2() {
            //     const path = 'http://127.0.0.1:5000/get_features';
            //     axios.get(path)
            //         .then((res) => {
            //             console.log(res.data);
            //         })
            // },
            // test() {
            //     const path = 'http://127.0.0.1:5000/table_massage';
            //     axios.get(path)
            //         .then((res) => {
            //             console.log(res.data);
            //         })
            // },

            handleCreate() {
                if (this.value1 == false){
                    this.$message.error('请先开启摄像头');
                    return false
                }
                this.thisContext.drawImage(this.thisVideo, 0, 0, this.videoWidth, this.videoHeight)
                // 获取图片base64链接
                var image = this.thisCancas.toDataURL('image/png')
                this.imgData = image.replace(/^data:image\/(png|jpg);base64,/,"")
                this.Form = {
                    name: "未知",
                    sex: "男",
                    age: "未知",
                    phone: "未知",
                };
                this.dialogFormVisible = true;
                console.log(this.Form)
            },

            image_cap() {
                if (this.value1 == false){
                    this.$message.error('请先开启摄像头');
                    return false
                }
                const url = 'http://127.0.0.1:5000/receiveImage';
                // 点击，canvas画图
                this.thisContext.drawImage(this.thisVideo, 0, 0, this.videoWidth, this.videoHeight)
                // 获取图片base64链接
                var image = this.thisCancas.toDataURL('image/png')
                image = image.replace(/^data:image\/(png|jpg);base64,/,"")
                axios({
                    method: 'post',
                    url:url ,
                    data:{
                        imgData:image
                    }
                })
                    .then( (response) => {
                        console.log(response);
                        if (response.data.name == null) {
                            this.$message.error('未检测到人脸');
                            return false
                        }
                        this.face.name = response.data.name
                        this.face.age = response.data.age
                        this.face.sex = response.data.sex
                        this.face.phone = response.data.phone
                        this.face.id = response.data.id
                        this.face.credit = response.data.credit
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            },
            put_loan() {
                if (this.loan.monovalent=="" || this.loan.time=="") {
                    this.$message({
                        message: "请完整填写申请",
                        type: "error",
                    })
                    return false
                }
                if (this.face.id=="未知") {
                    this.$message({
                        message: "请先进行人脸识别",
                        type: "error",
                    })
                    return false
                }
                const url = 'http://127.0.0.1:5000/loan_from';
                axios({
                    method: 'post',
                    url:url ,
                    data:{
                        id:this.face.id,
                        monovalent:this.loan.monovalent,
                        work_id:this.$store.state.work_id,
                        time:this.loan.time,
                        status:this.loan.status,
                    }
                })
                    .then((res) => {
                        console.log(res.data);
                        this.$message({
                            message:res.data.result,
                            type:res.data.type
                        });
                    })
            },
            getTime(date){
                this.loan.time = date;
                console.log(this.loan.time)
            }
        }
    };
</script>

<style scoped>

.grid-content {
    display: flex;
    align-items: center;
    height: 100px;
}
.grid-face {
    display: flex;
    align-items: center;
    height: 300px;
}

.grid-cont-right {
    flex: 1;
    text-align: center;
    font-size: 14px;
    color: #999;
}

.grid-num {
    font-size: 30px;
    font-weight: bold;
}

.grid-con-icon {
    font-size: 50px;
    width: 100px;
    height: 100px;
    text-align: center;
    line-height: 100px;
    color: #fff;
}

.grid-con-1 .grid-con-icon {
    background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
    background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
    color: rgb(100, 213, 114);
}

.grid-con-3 .grid-con-icon {
    background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
    color: rgb(242, 94, 67);
}

.user-info {
    display: flex;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 2px solid #ccc;
    margin-bottom: 20px;
}

.user-avator {
    width: 120px;
    height: 120px;
    border-radius: 50%;
}

.user-info-cont {
    padding-left: 50px;
    flex: 1;
    font-size: 14px;
    color: #999;
}

.user-info-cont div:first-child {
    font-size: 30px;
    color: #222;
}


.user-info-list span {
    margin-left: 70px;
}

.mgb20 {
    margin-bottom: 20px;
}
.circle-credit {
    position: relative;
}

</style>
