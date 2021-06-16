import pymysql as MySQLdb
import time
def db_connect():# 数据库连接
    db = MySQLdb.connect(host="localhost",port=3306, user="root",password="123456",database="face_data",charset='utf8' )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    return cursor,db

def db_close(cursor,db):# 数据库关闭
    cursor.close()
    db.close()

def user_search(account):#查找密码
    cursor, db = db_connect()
    sql = """select passwd,work_id from user where account = %s"""
    try:
        cursor.execute(sql,account)
        ((result),) = cursor.fetchall()
        return result
    except Exception as e:
        db.rollback()
    db_close(cursor, db)

def face_info_search(id):#查找客户信息
    cursor, db = db_connect()
    sql = """select * from client_massage where id = %s"""
    try:
        cursor.execute(sql,id)
        # ((result,),) = cursor.fetchall()
        result = cursor.fetchall()
        print(result)
        return result
    except Exception as e:
        db.rollback()
    db_close(cursor, db)

def loan_info_search(id):#查找借贷信息
    cursor, db = db_connect()
    sql = """select * from loan where id = %s"""
    try:
        cursor.execute(sql,id)
        result = cursor.fetchall()
        return result
    except Exception as e:
        db.rollback()
    db_close(cursor, db)

def face_info_del(id):#删除客户信息
    cursor, db = db_connect()
    sql = """delete from client_massage where id = %s"""
    try:
        cursor.execute(sql,id)
        db.commit()
        return 'success'
    except Exception as e:
        db.rollback()
        return 'error'
    db_close(cursor, db)

def face_info_edi(name,age,phone_number,sex,id):#更改客户信息
    cursor, db = db_connect()
    sql = """update client_massage set name = %s,age = %s,phone_number = %s, sex = %s where id = %s"""
    try:
        cursor.execute(sql,[name,age,phone_number,sex,id])
        db.commit()
        return 'success'
    except Exception as e:
        db.rollback()
        return 'error'
    db_close(cursor, db)

def face_all_info_search():#查找所有客户信息
    cursor, db = db_connect()
    sql = """select * from client_massage """
    try:
        cursor.execute(sql)
        # ((result,),) = cursor.fetchall()
        result = cursor.fetchall()
        print(result)
        return result
    except Exception as e:
        db.rollback()
    db_close(cursor, db)

def user_insert(account,passwd,id):#插入账号信息，注册
    cursor,db = db_connect()
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = """INSERT INTO user(account,passwd,work_id,resgister_date) values(%s,%s,%s,%s)"""
    try:
        print([account,passwd,id])
        cursor.execute(sql,[account,passwd,id,date])
        db.commit()
        result = 'success'
    except Exception as e:
        db.rollback()
        result = 'error'
    db_close(cursor, db)
    return result

def insert_client(name,age,phone_number,sex,bank_number,identity,img,):#插入客户信息
    cursor,db = db_connect()
    sql = """INSERT INTO client_massage(name,age,phone_number,sex,client_date,bank_number,identity) values(%s,%s,%s,%s,%s,%s,%s)"""
    try:
        print(name,age,phone_number,sex)
        # cursor.execute(sql,[name,age,phone_number,sex,(MySQLdb.Binary(img))])
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor.execute(sql, [name, age, phone_number, sex,date,bank_number,identity,])
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db_close(cursor, db)
    return True

def loan_insert(id,monovalent,work_id,statu,deathtime):#插入借贷信息
    cursor,db = db_connect()
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(id,monovalent,work_id,date,statu,deathtime)
    sql = """INSERT INTO loan(id,monovalent,work_id,time,statu,deathtime) values(%s,%s,%s,%s,%s,%s)"""
    try:
        cursor.execute(sql,[id,monovalent,work_id,date,statu,deathtime])
        db.commit()
        result = 'success'
    except Exception as e:
        db.rollback()
        result = 'error'
    db_close(cursor, db)
    return result

if __name__ == '__main__':
    print()