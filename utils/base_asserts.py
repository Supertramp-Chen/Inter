# -*- coding:utf-8 -*-
from utils.get_keywords import GetKeywords
import pytest
import logging
"""多重断言在excel中的写法
{"status_code":200,
"code":200,
"time":100,
"str":("成功","success"),
"type":({"check_name":"available","check_type":bool,"index":"all"},{"check_name":"pageSize","check_type":int,"index":0})}
str的value需要是元组 如果只有一个则写为"str"=("成功",)
type的value为字典元组"""
class BaseAsserts:
    @staticmethod
    def status_code_assert(status_code,result):
        """
        做返回值的状态码的断言方式
        :param status_code: 预期结果状态码
        :param result: 实际结果
        :return:布尔值
        """
        res = GetKeywords.get_keyword(result,"status_code")
        return res == status_code


    @staticmethod
    def code_assert(code,result):
        """
        返回值的code码的断言
        :param code: 预期结果code码
        :param result: 实际结果
        :return:
        """
        res = GetKeywords.get_keyword(result, "code")
        return res == code

    @staticmethod
    def str_assert(check_name,result):
        """
        判断字符串是否存在响应的结果里面
        :param check_name: 预期的结果
        :param result: 实际的返回值
        :return: 布尔值
        """
        return check_name in str(result)

    @staticmethod
    def time_assert(response_time,excepted_time):
        """
        响应时间的断言
        :param response_time: 实际接口的响应时间
        :param excepted_time: 预期的响应时间
        :return:
        """
        return response_time <= excepted_time

    @staticmethod
    def type_assert(excepted_type,check_name):
        """
        类型断言
        :param excepted_type: 预期的类型
        :param check_name:检查的字段
        :return:
        """
        return isinstance(check_name,excepted_type)

# 判断什么情况下调用什么方法
class MainAsserts(BaseAsserts):
    def __init__(self,case,result):
        # 是否是私有和实现的逻辑没有任何关系，
        # 只是更加符合面向对象的“封装”的思想
        # 面向对象三大特征：封装，继承，多态
        # self.__base = BaseAsserts()
        self.__case = case
        self.__result = result

    def main_assert(self):
        for key, value in eval(self.__case["check"]).items():
            if key == "status_code":
                logging.info(f"3.HTTP多重响应断言内容(status_code): 预期结果({value}) ?in 实际结果({self.__result})")
                pytest.assume(self.status_code_assert(value,self.__result))
            if key == "code":
                logging.info(f"3.HTTP多重响应断言内容(code): 预期结果({value}) ?in 实际结果({self.__result})")
                pytest.assume(self.code_assert(value,self.__result))
            if key == "str":
                # 写成元组的形式 因为我们做断言的时候，可能会去断言多个字符串是否存在返回值
                # 所以这边写成元组的形式，然后把元组遍历出来
                for v in value:
                    logging.info(f"3.HTTP多重响应断言内容(str): 预期结果({v}) ?in 实际结果({self.__result})")
                    pytest.assume(self.str_assert(v,self.__result))

            if key == "time":
                response_time = GetKeywords.get_keyword(self.__result,"response_time")
                logging.info(f"3.HTTP多重响应断言内容(time): 预期结果({value}) ?>= 实际结果({response_time})")
                pytest.assume(self.time_assert(response_time,value))

            if key == "type":
                for v in value:
                    # 1.在返回值里面不只是一个字段需要做类型断言
                        # type对应的value为元组字典
                    check_name = v.get("check_name")
                    check_type = v.get("check_type")
                    index = v.get("index")

                    if index == "all":
                        # 2.返回的字段里面，某一个字段，可能有多个值，都需要断言
                            # 多个值都需要断言，因此新增一个index为all的逻辑
                        res_list = GetKeywords.get_keywords(self.__result,check_name)
                        # 列表需要去循环出来，然后放到新的类型列表里面去，然后再逐个判断
                        for res in res_list:
                            logging.info(f"3.HTTP多重响应断言内容(type): 预期结果({check_type}) ?in 实际结果({res})")
                            pytest.assume(self.type_assert(check_type, res))

                    if isinstance(index,int):
                        # 通过index去获取第几个数据进行断言
                        res = GetKeywords.get_keyword(self.__result,check_name,index)
                        logging.info(f"3.HTTP多重响应断言内容(type): 预期结果({check_type}) ?in 实际结果({res})")
                        pytest.assume(self.type_assert(check_type,res))