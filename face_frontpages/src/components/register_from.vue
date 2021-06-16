<template>
    <el-drawer
            title="请完善您的注册信息"
            :visible.sync="dialog"
            direction="rtl"
            custom-class="demo-drawer"
            ref="drawer"
            size="30%"
    >
        <div class="demo-drawer__content" style="padding: 30px;">
            <el-form :model="User" :rules="rules" label-width="60px" >
                <el-form-item label="姓名" prop="account" :label-width="formLabelWidth">
                    <el-input size="medium" v-model="User.account" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="passwd"  :label-width="formLabelWidth">
                    <el-input size="medium" placeholder="请输入密码" v-model="User.passwd" show-password></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="ex_passwd" :label-width="formLabelWidth">
                    <el-input size="medium" placeholder="请确认输入密码" v-model="User.ex_passwd" show-password></el-input>
                </el-form-item>
                <el-form-item label="工号" prop="id" :label-width="formLabelWidth">
                    <el-input size="medium" placeholder="请输入工号" v-model="User.id"></el-input>
                </el-form-item>
            </el-form>
            <div class="demo-drawer__footer">
                <el-button @click="cancelForm">取 消</el-button>
                <el-button type="primary" @click="addUser();$refs.drawer.closeDrawer();" :loading="loading">{{ loading ? '提交中 ...' : '确 定' }}</el-button>
            </div>
        </div>
    </el-drawer>
</template>
<script>
    import axios from 'axios'
    export default {
        name: "register_from",
        props:["dialog_login"],
        data() {
            return {
                dialog:this.dialog_login,
                loading: false,
                User: {
                    account: '',
                    passwd: '',
                    ex_passwd:'',
                    id:'',
                },
                rules: {
                    account: [
                        { required: true, message: '请输入账号', trigger: 'blur' },
                    ],
                    passwd: [
                        { required: true, message: '请输入密码', trigger: 'blur' },
                    ],
                    ex_passwd: [
                        { required: true, message: '请再次输入密码', trigger: 'blur' },
                    ],
                    id: [
                        { required: true, message: '请输入工号', trigger: 'blur' },
                        { min: 4, max: 4, message: '长度错误', trigger: 'blur' },
                    ],

                },
                formLabelWidth: '80px',
                timer: null,
            };
        },
        methods: {
            cancelForm() {
                this.loading = false;
                this.dialog = false;
                clearTimeout(this.timer);
            },
            outing(){
                this.dialog=true
            },
            addUser(){
                const url = 'http://127.0.0.1:5000/register'
                axios({
                    method: 'post',
                    url:url ,
                    data: {
                        account: this.User.account,
                        passwd: this.User.passwd,
                        id:this.User.id,
                    }
                })
                    .then( (response) => {
                        console.log(response);
                        this.$message({
                            message:response.data.result,
                            type: response.data.result
                        });
                    })
                    .catch((error) => {
                        console.log(error);
                        this.$message.error('注册失败');
                    });
            }
        },
    }
</script>

<style scoped>

</style>