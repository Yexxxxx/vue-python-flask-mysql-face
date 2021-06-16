var sqlMap = {
    // 用户
    user: {
        search:'select passwd from user where account = ?',
        add: 'insert into user values (?,?)'
    },
    other:{
        delete:'', // delete sql语句
        post: '',
        get: ''
    }

}

module.exports = sqlMap;