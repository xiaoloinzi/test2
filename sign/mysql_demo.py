# encoding=utf-8
from pymysql import cursors,connect
'''
connect():建立数据库连接
cursor():获取数据库操作游标
execute():执行SQL语句
commit():提交数据库执行
close():关闭数据库连接
'''
#
# 连接数据库
conn = connect(host = '127.0.0.1',
               user='root',
               password ='',
               db='guest',
               charset = 'uttf8bm4',
               cursorclass = cursors.DictCursor)
try:
    with conn.cursor() as cursor:
        # 创建嘉宾表
        sql = 'INSERT ONTO sign_guest(realname,phone,email,sign,event_id,create_time) VALUES ("tom",18800110002,"tom@163.com",0,1,NOW());'
        cursor.execute(sql)
        # 提交事务
        conn.commit()
    with conn.cursor() as cursor:
        sql = "select realname,phone,email,sign from sign_guest WHERE phone=%s"
        cursor.execute(sql,('18800110002',))
        result = cursor.fetchone()
        print(result)
finally:
    conn.close()