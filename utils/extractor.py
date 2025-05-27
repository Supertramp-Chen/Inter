import logging
import allure
from utils.send_request import send_jdbc_request
from utils.get_keywords import GetKeywords
import re

def json_extractor(case, all, res):
    if case["jsonExData"]:
        with allure.step("4.JSON提取"):
            # 首先要把 jsonExData 的 key, value 拆开
            for key, value in eval(case["jsonExData"]).items():
                # value = jsonpath.jsonpath(res.json(), value)[0]

                value = GetKeywords.get_keyword(res,value)
                # print(key)
                # print(value)
                all[key] = value
                # print(all)
            logging.info(f"4.JSON提取, 根据{case['jsonExData']}提取数据, 此时全局变量为: {all}")


def jdbc_extractor(case, all):
    if case["sqlExData"]:
        with allure.step("4.JDBC提取"):
            for key, value in eval(case["sqlExData"]).items():
                # print(key)
                # print(value)
                value = send_jdbc_request(value)
                # print(value)
                all[key] = value
                # print(all)
            logging.info(f"4.JDBC提取, 根据{case['sqlExData']}提取数据, 此时全局变量为: {all}")


# 单独写一个方法/函数来处理正则表达式
def re_match_value(string,pattern,index=0):
    """
    正则表达式提取值
    :param string: 字符串
    :param pattern: 正则表达式
    :param index: 获取第几个值，默认是0
    :return:
    """
    # matches = []
    #
    # for match in re.finditer(pattern,string):
    #     matches.append(match.group())
    # 列表推导式简化代码
    matches = [match.group(1) for match in re.finditer(pattern,string)]
    return matches[index]


def re_extractor(case,all,res):
    if case["reExData"]:
        with allure.step("4.正则提取"):
            for key,value in eval(case["reExData"]).items():
                # value:表达式
                v = re_match_value(str(res),value)
                all[key] = v

            logging.info(f"4.正则提取, 根据{case['reExData']}提取数据, 此时全局变量为: {all}")
