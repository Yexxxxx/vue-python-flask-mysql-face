<template>

    <div id="login_card">

        <el-row >
            <el-col style="margin-left: 34%;" :span="8" v-for="(o, index) in 1" :key="o" :offset="index > 0 ? 2 : 0">
                <el-card  :body-style="{ padding: '0px' }">
                    <div style="padding: 30px;">
                        <el-avatar :size="70"> user </el-avatar>
                    </div>
                    <div style="padding: 30px;">
                        <el-form :label-position="labelPosition" label-width="70px" :model="User" :rules="rules" method="post">
                            <el-form-item label="账号" prop="account">
                                <el-input size="medium" placeholder="请输入账号" v-model="User.account" ></el-input>
                            </el-form-item>
                            <el-form-item label="密码" prop="passwd">
                                <el-input size="medium" placeholder="请输入密码" v-model="User.passwd"  show-password></el-input>
                            </el-form-item>
                            <el-form-item label="验证码" >
                                <el-input size="medium" placeholder="请输入验证码"  v-model="input_vaild_value"></el-input>
                                <Validcode @getvaildcode="getvaildcode" ref="valid"></Validcode>
                            </el-form-item>
                                <el-button  type="primary" @click="vaild_check()" size="medium">登入</el-button>
                                <el-button size="medium" @click="register()" round>注册</el-button>
                        </el-form>
                    </div>
                </el-card>
            </el-col>
        </el-row>
        <Register_from ref="Register_from"></Register_from>

    </div>
</template>
<script>
    import Register_from from "./register_from";
    import Validcode from "./Vaildcode";
    import axios from 'axios'
    export default {
        name: "Login_card",
        components: {
            Register_from,
            Validcode
        },
        data() {
            return {
                dialog:false,
                labelPosition: 'right',
                passwd_db:'',
                input_vaild_value:'',
                vaild_value:'',
                User: {
                    account: '',
                    passwd: '',
                    work_id:'',
                },
                rules: {
                    account: [
                        { required: true, message: '请输入账号', trigger: 'blur' },
                    ],
                    passwd: [
                        { required: true, message: '请输入密码', trigger: 'blur' },
                    ],

                },
            };
        },
        methods:{
            register(){
                this.$refs.Register_from.outing()
            },
            login(){
                const url = 'http://127.0.0.1:5000/login'
                axios({
                    method: 'post',
                    url:url ,
                    data: {
                        account: this.User.account,
                        passwd: this.User.passwd,
                    }
                })
                    .then( (response) => {
                        console.log(response);
                        this.User.work_id = response.data.work_id
                        this.passwd_check(response.data.flag)
                    })
                    .catch((error) => {
                        console.log(error);
                        this.open_error()
                    });
            },
            passwd_check(flag) {
                if (flag == true){//密码判断
                    this.open_pass()
                    return true
                }
                else{
                    console.log(false);
                    this.open_error()
                    return false
                }
            },
            vaild_check(){
              if  ( this.input_vaild_value != this.vaild_value){
                  this.$message.error('验证码错误');
                  this.$refs.valid.createdCode();
              }
              else {
                  this.login()
              }
            },
            open_error() {
                this.$message.error('此账号未注册或密码错误');
            },
            open_pass() {
                this.$store.commit('account_updata',this.User.account)
                this.$store.commit('work_id_updata',this.User.work_id)
                this.$router.push({path: '/Home'});//页面跳转入管理页面
                this.$message({
                    message: '登入成功',
                    type: 'success'
                });
            },
            getvaildcode(data){
                this.vaild_value=data
            },

        },
        watch:{
        }

    }
</script>

<style scoped>
    #login_card{

    }



</style>