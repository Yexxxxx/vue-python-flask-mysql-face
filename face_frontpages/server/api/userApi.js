var models = require('../db');
var express = require('express');
var router = express.Router();
var mysql = require('mysql');
var $sql = require('../sqlMap');

// 连接数据库

function handleError () {
    //创建一个mysql连接对象
    conn = mysql.createConnection(models.mysql)

    //连接错误，2秒重试
    conn.connect(function (err) {
        if (err) {
            console.log('error when connecting to db:', err);
            setTimeout(handleError , 2000);
        }
    });
    //监听错误
    conn.on('error', function (err) {
        console.log('db error', err);
        // 如果是连接断开，自动重新连接
        if (err.code === 'PROTOCOL_CONNECTION_LOST') {
            handleError();
        } else {
            throw err;
        }
    });
}
handleError();


var jsonWrite = function(res, ret) {
    if(typeof ret === 'undefined') {
        res.json({
            code: '1',
            msg: '操作失败'
        });
    } else {
        res.json({
            code: '0',
            msg: '操作成功'
        })

    }
};

router.get('/getUser', (req, res) => {
    var sql = $sql.user.search
    var account = req.query.account
    conn.query(sql,account,function (err, result) {
        if (err) {
            console.log(err)
        }
        if (result) {
            console.log(result)
            res.send(result)
        }
    })
})
// 增加用户接口
router.post('/addUser', (req, res) => {
    var sql = $sql.user.add;
    var params = req.body;
    console.log(params);
    conn.query(sql,[params.account, params.passwd], function(err, result) {
        if (err) {
            console.log(err);
        }
        if (result) {
            jsonWrite(res, result);
            console.log("插入成功")
        }
    })
});

module.exports = router;