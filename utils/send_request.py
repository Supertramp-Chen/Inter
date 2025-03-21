import logging

import allure
import pymysql
import requests
from config.config import *


@allure.step("2.发送HTTP请求")
def send_http_request(**request_data):
    """
    res 是 requests.Response 对象
	res.text 是 字符串格式的数据（可能是 JSON、HTML 或其他
	res.json() 是 JSON 解析后的 Python dict 对象
    """
    res = requests.request(**request_data)
    response = {
        "status_code": res.status_code,
        "json_data": res.json(),
        "response_time": res.elapsed.total_seconds() * 1000
    }
    logging.info(f"2.发送HTTP请求, 响应内容为: {response}")
    # logging.info(f"2.发送HTTP请求, 响应文本为: {res.text}")
    return res


def send_jdbc_request(sql, index=0):
    conn = pymysql.Connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        charset="utf8"
    )
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[index]
