import pymysql
from pymysql.cursors import DictCursor
from config.config import *
import logging
from apiException.custom_exception import *

"""
封装对 MySQL 数据库的连接 查询 修改操作"""
class Database:
    def __init__(self):
        # 因为只在内部会去访问这个self.__db
        # 因此可以把它设置为私有属性
        """
        创建 Database 类时，会自动调用 __getConnet() 方法建立数据库连接。
	    self.__db 是 私有属性，外部不能直接访问，表示数据库连接对象
        私有连接属性，通过 __getConnet() 初始化。
	    出错时抛出自定义异常，方便排查问题"""
        self.__db = self.__getConnet()

    '''静态方法：直接用 类名.方法名() 调用，不需要实例化对象
    🔸 因为 __getConnet() 既不访问对象属性（self），也不访问类属性（cls），
    🔸 它只负责根据固定的配置返回一个数据库连接。
    🔸 用静态方法的方式定义，更清晰、简洁、高效。'''
    @staticmethod
    def __getConnet():
        # 建立数据库连接
        # 创建连接对象的方法
        """
        pymysql.Connect 创建连接，使用配置（DB_HOST、DB_USER等）连接数据库。
	•	autocommit=True 表示每次操作后自动提交（否则需要手动 commit）。
	•	如果连接失败，记录日志并抛出自定义异常 DatabaseException。
        """
        try:
            conn = pymysql.Connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                charset="utf8",
                autocommit=True #如果没设置 autocommit=True，那么数据库连接默认开启事务，执行 SQL 后必须 显式调用 conn.commit()，否则修改不会生效。

            )
            return conn
        except Exception as e:
            logging.error(f"数据库连接失败, 错误异常是: {e}")
            raise DatabaseException()
    """
    •	执行传入的 SQL 查询（sql）。
	•	使用 DictCursor，返回的是 字典形式，而不是元组。
	•	返回查询到的 一行数据（字典形式）
	get_one 查询一行数据（返回字典）。"""
    def get_one(self,sql):
        try:
            if self.__db:
                # 执行sql，需要返回值--查询
                with self.__db.cursor(DictCursor) as cur:
                    cur.execute(sql)
                    return cur.fetchone()
        except Exception as e:
            logging.error(f"数据库查询失败, 错误异常是: {e}")
            raise GetDataException()
    """
    •	接收 多个 SQL 语句（*sqls 不定参数，打包为元组）。
	•	依次执行每条语句（比如更新、删除语句）。
	•	如果出错，抛出 ExecuteSqlException。
	execute_sql 执行多个更新/删除语句"""
    def execute_sql(self,*sqls):  # *参数，表示不定传参，打包成一个元组
        try:
            # 执行sql，不需要返回值--删除，修改
            if self.__db:
                with self.__db.cursor(DictCursor) as cur:
                    for sql in sqls:
                        cur.execute(sql)

        except Exception as e:
            logging.error(f"数据库修改，删除失败, 错误异常是: {e}")
            raise ExecuteSqlException()





if __name__ == '__main__':
    db = Database()
    # SQL1 = 'UPDATE base_data_product_brand set NAME = "大米" where code = 001'
    # SQL2 = 'select * from tbl_shop'
    SQL1 = 'select * from sp_user'
    SQL2 = 'select * from sp_order'
    db.execute_sql(SQL1)
    print(db.get_one(SQL1))
    # print(db.get_one("select `code1` from base_data_product_brand"))



