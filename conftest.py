import pytest

from config.config import *
from utils.database import Database
'''
前置+后置操作：测试用例执行完之后自动调用next函数然后执行yield后面的后置操作
conftest里用fixture+生成器 编写数据清除函数 实现测试用例执行完后自动清除数据
    连接数据库 执行sql
		conn=pymysql.Connect(参数)创建数据库连接 
		cur=conn.cursor()创建游标 
		写个for循环执行sql cur.execute()
		关闭连接和游标'''
@pytest.fixture(scope="session", autouse=True)
def destroy_data():
    print("wwwww")
    yield
    Database().execute_sql(SQL1,SQL2)
    # sqls = [SQL1, SQL2]
    #
    # conn = pymysql.Connect(
    #     host=DB_HOST,
    #     port=DB_PORT,
    #     database=DB_NAME,
    #     user=DB_USER,
    #     password=DB_PASSWORD,
    #     charset="utf8",
    #     autocommit=True
    # )
    # cur = conn.cursor()
    #
    # for sql in sqls:
    #     cur.execute(sql)
    #
    # cur.close()
    # conn.close()
