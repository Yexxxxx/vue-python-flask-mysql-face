<template>
    <div>
        <div class="container">

            <el-table
                    :data="tempList"
                    border
                    class="clinet_table"
                    ref="multipleTable"
                    header-cell-class-name="table-header"
                    @selection-change="handleSelectionChange"
            >
                <el-table-column type="selection" width="55" align="center"></el-table-column>
                <el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
                <el-table-column prop="name" label="姓名"></el-table-column>
                <el-table-column prop="sex" label="性别"></el-table-column>
                <!--<el-table-column prop="img" label="训练图片预览" align="center">-->
                    <!--<template >-->
                        <!--<el-image-->
                                <!--class="table-td-thumb"-->
                                <!--:src="require('../assets/1.jpg')"-->
                        <!--&gt;</el-image>-->
                    <!--</template>-->
                <!--</el-table-column>-->
                <el-table-column prop="phone" label="联系电话"></el-table-column>
                <el-table-column prop="bank_number" label="银行卡号"></el-table-column>
                <el-table-column prop="identity" label="身份证号"></el-table-column>
                <el-table-column prop="time" label="创建时间"></el-table-column>
                <el-table-column label="借贷详情">
                    <template slot-scope='scope'>
                        <el-button
                                type="text"
                                icon="el-icon-tickets"
                                @click="get_loan_data(scope.row.id)"
                        >详情</el-button>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope='scope'>
                        <el-button
                                type="text"
                                icon="el-icon-edit"
                                @click="handleEdit(scope.row)"
                        >编辑</el-button>
                        <el-button
                                type="text"
                                icon="el-icon-delete"
                                class="red"
                                @click="handleDelete(scope.row.id)"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <!--<div class="foot-box">-->
                <!--<el-button-->
                        <!--type="primary"-->
                        <!--icon="el-icon-delete"-->
                        <!--class="handle-del mr10"-->
                        <!--@click="delAllSelection"-->
                <!--&gt;批量删除</el-button>-->
            <!--</div>-->
            <div class="pagination">
                <el-pagination
                        background
                        layout="total, prev, pager, next"
                        :current-page="pageIndex"
                        :page-size="pageSize"
                        :total="tableData.length"
                        @current-change="handleCurrentChange"
                ></el-pagination>
            </div>
        </div>

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
            <el-form ref="form" :model="form" label-width="70px">
                <el-form-item label="姓名">
                    <el-input v-model="form.name"></el-input>
                </el-form-item>
                <el-form-item label="年龄">
                    <el-input v-model="form.age"></el-input>
                </el-form-item>
                <el-form-item label="性别">
                    <el-input v-model="form.sex"></el-input>
                </el-form-item>
                <el-form-item label="电话">
                    <el-input v-model="form.phone"></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="editVisible = false">取 消</el-button>
                    <el-button type="primary" @click="saveEdit">确 定</el-button>
                </span>
            </template>
        </el-dialog>
        <!-- 详情弹出框 -->
        <el-dialog title="借贷详情" :visible.sync="detailVisible" width="30%">
            <el-table :data="loan_list">
                <el-table-column prop="monovalent" label="借贷额度" ></el-table-column>
                <el-table-column prop="deathtime" label="还款日期"></el-table-column>
                <el-table-column prop="work_id" label="审查者"></el-table-column>
                <el-table-column prop="statu" label="发放状态"></el-table-column>
            </el-table>
        </el-dialog>
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        name: "table",
        data() {
            return {

                pageIndex: 1,
                pageSize: 10,
                pageTotal: 0,

                tableData: [],
                tempList:[],
                multipleSelection: [],
                delList: [],
                editVisible: false,
                detailVisible: false,
                form: {
                    name: "",
                    sex: "",
                    age: "",
                    phone: "",
                    id:"",
                    time:"",
                    bank_number:'',
                    identity:'',
                },
                loan_list:[],
                idx: -1,
                id: -1
            };
        },
        created() {
            this.get_user_data();

        },
        mounted(){

        },
        methods: {
            // 获取模拟数据
            get_user_data() {
                const path = 'http://127.0.0.1:5000/table_massage';
                axios.get(path)
                    .then((res) => {
                        console.log(res.data);
                        this.tableData = res.data.result
                        this.handleCurrentChange(this.pageIndex)

                    })
            },
            get_loan_data(id) {
                console.log(id)
                const path = 'http://127.0.0.1:5000/loan_massage';
                axios({
                    method: 'post',
                    url:path ,
                    data:{
                        id:id,
                    }
                })
                    .then((res) => {
                        console.log(res.data);
                        this.loan_list = res.data.result
                        this.detailVisible = true
                    })
            },
            // 删除操作
            handleDelete(index) {
                // 二次确认删除
                this.$confirm("确定要删除吗？", "提示", {
                    type: "warning"
                })
                    .then(() => {
                        // this.$message.success("删除成功");
                        this.tableData.splice(index, 1);
                        this.handledel(index)
                    })
                    .catch(() => {});
            },
            handledel(id) {
                const url = 'http://127.0.0.1:5000/table_massage_del';
                axios({
                    method: 'post',
                    url:url ,
                    data: {
                        id:id
                    }
                })
                    .then((res) => {
                        this.editVisible = false;
                        this.$message({
                            message:res.data.result,
                            type: res.data.type
                        });
                        this.get_user_data()
                    })
            },
            // 多选操作
            handleSelectionChange(val) {
                this.pageIndex = val;
            },
            // 编辑操作
            handleEdit(content) {
                this.editVisible = true;
                this.form.name = content.name
                this.form.age = content.age
                this.form.sex = content.sex
                this.form.phone = content.phone
                this.form.id = content.id
                this.form.time = content.time
                this.form.bank_number = content.bank_number
                this.form.identity = content.identity
            },

            // 保存编辑
            saveEdit() {
                const url = 'http://127.0.0.1:5000/table_massage_edit';
                axios({
                    method: 'post',
                    url:url ,
                    data: {
                        form:this.form
                    }
                })
                    .then((res) => {
                        this.editVisible = false;
                        this.$message({
                            message:res.data.result,
                            type: res.data.type
                        });
                        this.get_user_data()
                    })
            },

            handleCurrentChange(pageIndex) {//页码切换
                this.pageIndex = pageIndex
                this.currentChangePage(this.tableData,pageIndex)
            },
            //分页方法（重点）
            currentChangePage(list,pageIndex) {
                let from = (pageIndex - 1) * this.pageSize;
                let to = pageIndex * this.pageSize;
                this.tempList = [];
                for (; from < to; from++) {
                    if (list[from]) {
                        this.tempList.push(list[from]);
                    }
                }
            },
        }
    };
</script>

<style scoped>

    .clinet_table {
        width: 100%;
        font-size: 14px;
    }
    .red {
        color: #ff0000;
    }
    .table-td-thumb {
        display: block;
        margin: auto;
        width: 40px;
        height: 40px;
    }
</style>