# -*- coding: utf-8 -*-
import logging
import allure
import requests
from utils.database import Database
import time

"""
然后发送http请求 使用字典解包 
**requesdata 展开字典的key value去掉key的引号变成key=value的形式 作为参数传给函数 
用requests.request发送http请求 返回一个response对象res"""
@allure.step("2.发送HTTP请求")
def send_http_request(**request_data):
    # 判断是否需要等待
    url = request_data.get('url', '')
    # 这里以登录接口为例，你可以根据实际需求修改判断条件
    if '/login' in url:
        time.sleep(3)  # 只对登录请求添加3秒延时
        logging.info("登录请求等待3秒...")

    res = requests.request(**request_data)
    # print("res=", res.text, "\ntype-res=", type(res.text))
    response = {
        "status_code":res.status_code,# 状态码
        "json_data":res.json(),
        "response_time":res.elapsed.total_seconds() * 1000
    }
    logging.info(f"2.发送HTTP请求, 响应内容为: {response}")
    # print("response=", response, "\ntype-response=", type(response))
    return response


def send_jdbc_request(sql):
    # 使用Database类执行SQL查询
    return Database().get_one(sql)
    # conn = pymysql.Connect(
    #     host=DB_HOST,
    #     port=DB_PORT,
    #     database=DB_NAME,
    #     user=DB_USER,
    #     password=DB_PASSWORD,
    #     charset="utf8"
    # )
    # cur = conn.cursor()
    # cur.execute(sql)
    # result = cur.fetchone()
    # cur.close()
    # conn.close()
    # return result[index]