import logging
import allure
from utils.send_request import send_jdbc_request
from utils.get_keywords import GetKeywords
from utils.base_asserts import MainAsserts
from abc import ABC, abstractmethod
import pytest

'''多态：
不同子类对象可以用同一个父类引用来表示。
调用方法时，根据对象的真实类型，自动调用对应子类的方法。'''

"""定义 HTTP 断言的 抽象基类定义接口（父类）
所有断言类都要有http_assert()方法，具体实现由子类决定"""
class DataAssert(ABC):
    @abstractmethod
    def http_assert(self, case, res):
        pass

"""工厂函数根据case动态选择子类（实现多态）"""
def obj_processor(case):
    """
    对象处理，根据传入的case的不同，来返回不同的对象
    """
    try:
        # 可能出现异常的代码
        """'eval 就是把字符串当成Python表达式来解析
        'code' → ❌ 解析失败（抛异常） → 走单断言
        因为Python会把 'code' 当作变量名去解析。
但是程序里并没有定义一个变量 code，所以 Python解释器会抛出异常： NameError: name 'code' is not defined。
        {"code":200}' → ✅ 解析成 {"code":200} → 走多断言"""
        eval(case["check"])
    except:
        # 出现异常之后，表示断言不是字典，因此走老逻辑
        # 返回单个断言的对象
        return SingleAssert()
    else:
        # 没有出现异常，表示可以转成字典，走多重断言的逻辑
        return MultipleAssert()

"""调用时用父类引用（多态体现）：
这里obj是父类类型（DataAssert），但实际指向的对象可以是SingleAssert或MultipleAssert。
调用http_assert时，Python自动根据真实对象类型，调用对应实现"""
def http_assert(case, res):
    """
    真正的调用逻辑，后续无论怎么新增http返回值的断言，都是调用这个函数
    :param case: 测试用例
    :param res: 返回结果
    :return:
    """
    obj_processor(case).http_assert(case, res)

"""子类继承并实现方法（多态核心）
两个子类方法签名完全一样（都是http_assert(case, res)），但内部实现不同"""
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