import logging
import allure
from utils.send_request import send_jdbc_request
from utils.get_keywords import GetKeywords
from utils.base_asserts import MainAsserts
from abc import ABC, abstractmethod
import pytest
"""
json断言我二次封装了jsonpath，用了try来抓取异常 如果没有在响应数据里面没有找到
  （jsonpath二次封装：在响应断言中判断case[“check”]是否存在 不存在就判断expect是否在res.text里面，
   存在就使用二次封装的jsonpath把res.json(responsed变成dict)和check传入 提取res里面的目标字段
jsonpath二次封装让excel里的expect不用写$..code 通过jsonpath.jsonpath(case,f"$..{name}")
	然后使用try expect如果jsonpath没有找到抓取异常把result=false 判断result的值为false的话输出查找失败）
"""
"""定义 HTTP 断言的抽象基类"""
class DataAssert(ABC):
    @abstractmethod
    def http_assert(self, case, res):
        pass
def obj_processor(case):
    """
    对象处理，根据传入的case的不同，来返回不同的对象
    :return:
    """
    try:
        # 可能出现异常的代码
        eval(case["check"])
    except:
        # 出现异常之后，表示断言不是字典，因此走老逻辑
        # 返回单个断言的对象
        return SingleAssert()
    else:
        # 没有出现异常，表示可以转成字典，走多重断言的逻辑
        return MultipleAssert()
def http_assert(case, res):
    """
    真正的调用逻辑，后续无论怎么新增http返回值的断言，都是调用这个函数
    :param case: 测试用例
    :param res: 返回结果
    :return:
    """
    obj_processor(case).http_assert(case, res)
class SingleAssert(DataAssert):
    @allure.step("3.HTTP响应断言")
    def http_assert(self, case, res):
        if case["check"]:
            # result = jsonpath.jsonpath(res.json(), case["check"])[0]
            # 状态码：200 404 302 500 502
            # 部分接口：重定向  302
            result = GetKeywords.get_keyword(res, case["check"])
            logging.info(f"3.HTTP响应断言内容: 实际结果({result}) == 预期结果({case['expected']})")
            assert result == case["expected"]
        else:
            logging.info(f"3.HTTP响应断言内容: 预期结果({case['expected']}) in 实际结果({res.text})")
            # 因为返回的res现在是一个字典，没有text的方法
            # 因此这里把返回的字典转成字符串类型，进行断言判断
            # assert case["expected"] in res.text
            assert case["expected"] in str(res)
class MultipleAssert(DataAssert):
    @allure.step("3.HTTP多重响应断言")
    def http_assert(self, case, res):
        if case["check"]:
            MainAsserts(case, res).main_assert()






class BaseJdbcAssert(ABC):
    @abstractmethod
    def jdbc_assert(self, case):
        pass


class SingleJdbcAssert(BaseJdbcAssert):
    def jdbc_assert(self, case):
        """
        jdbc--java的叫法
        在python连接数据库使用的是pymysql
        """
        if case["sql_check"] and case["sql_expected"]:
            with allure.step("3.JDBC响应断言"):
                result = send_jdbc_request(case["sql_check"])
                # logging.info(f"3.JDBC响应断言内容: 实际结果({result}) == 预期结果({case['sql_expected']})")
                # assert result == case["sql_expected"]
                logging.info(f"3.JDBC响应断言内容: 实际结果(预期结果({case['sql_expected']} in {result})")

            assert case["sql_expected"] in str(result)


"""
	1.	解析 sql_check 和 sql_expected
	2.	循环执行多个 SQL 语句
	3.	断言 expected in result
	4.	pytest.assume() 让失败的断言不影响后续测试"""
class MultipleJdbcAssert(BaseJdbcAssert):
    """多重数据库断言"""

    def jdbc_assert(self, case):
        if case["sql_check"] and case["sql_expected"]:
            with allure.step("3.JDBC多重响应断言"):
                sql_check = eval(case["sql_check"])
                sql_expected = eval(case["sql_expected"])
                for sql, expected in zip(sql_check, sql_expected):
                    result = send_jdbc_request(sql)
                    logging.info(f"3.JDBC多重响应断言内容: 实际结果(预期结果({expected} in {result})")
                    pytest.assume(expected in str(result))


def obj_jdbc_processor(case):
    """
    对象处理，根据传入的case的不同，来返回不同的对象
    :return:
    """
    try:
        eval(case["sql_check"])
    except:
        return SingleJdbcAssert()
    else:
        return MultipleJdbcAssert()


def jdbc_assert(case):
    """
    jdbc真正的断言逻辑
    :param case: 测试用例
    :return:
    """
    obj_jdbc_processor(case).jdbc_assert(case)