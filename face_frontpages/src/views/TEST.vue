<template>
    <div class="tab-container">
                {{data}}
                <el-button type="primary" @click="send()">确 定</el-button>
    </div>
</template>
<script>

    export default {
        data() {
            return {
                data:"",
            };
        },
        sockets: {
            connect: function () {
                console.log('socket 连接成功')
            },
            api: function (data) {
                console.log(data);
                this.data = data

            },
        },
        mounted(){
            this.$socket.connect()
            this.$socket.emit('test')
            console.log('连接中')
        },
        destroyed () {    // 当离开组件时，结束调用
            if (this.$socket) this.$socket.disconnect()  // 如果socket连接存在，销毁socket连接
            console.log('连接已断开')
        },

            methods: {
                send(){
                    this.$socket.emit('test',"发送后端")
                },
            },
    };
</script>
<style scoped>
</style>