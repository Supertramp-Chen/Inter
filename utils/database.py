# -*- coding:utf-8 -*-
# 北梦测教育
# 课程咨询加微信：xiaobeiceshi

import pymysql
from pymysql.cursors import DictCursor
from config.config import *
import logging
from apiException.custom_exception import *

class Database:
    def __init__(self):
        # 因为只在内部会去访问这个self.__db
        # 因此可以把它设置为私有属性
        self.__db = self.__getConnet()

    @staticmethod
    def __getConnet():
        # 创建连接对象的方法
        try:
            conn = pymysql.Connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                charset="utf8",
                autocommit=True
            )
            return conn
        except Exception as e:
            logging.error(f"数据库连接失败, 错误异常是: {e}")
            raise DatabaseException()

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
    SQL1 = 'UPDATE base_data_product_brand set NAME = "大米" where code = 001'
    # SQL2 = 'select * from tbl_shop'
    db.execute_sql(SQL1)
    # print(db.get_one("select `code1` from base_data_product_brand"))



