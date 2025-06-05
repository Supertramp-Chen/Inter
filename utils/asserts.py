import logging
import allure
from utils.send_request import send_jdbc_request
from utils.get_keywords import GetKeywords
from utils.base_asserts import MainAsserts
from abc import ABC, abstractmethod
import pytest

"""多态：
不同子类对象 继承同一个父类接口；
调用相同方法名，Python根据对象真实类型，自动调用对应的子类实现
✅ 通过 父类（抽象类）定义接口，不同子类实现不同的断言逻辑。
✅ 工厂函数 根据 case 内容动态选择子类（单断言或多断言）。
✅ 调用时通过父类接口调用方法，Python根据对象真实类型自动调用对应子类方法（多态）。
✅ 所有HTTP断言调用都只需调用 http_assert(case, res)，而不需要关心背后是单断言还是多断言。
✅ 解耦：调用者不需要知道用哪个断言对象，obj_processor会自动选择。
✅ 易扩展：未来增加新断言类型，只需在 obj_processor 中加判断，外部调用完全不用变。"""

"""✅ 整个 HTTP 响应断言的统一入口（统一接口 + 多态）
后续无论怎么新增http返回值的断言，都是调用这个函数"""
def http_assert(case, res):
    obj_processor(case).http_assert(case, res)

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

"""定义HTTP断言的抽象基类接口（父类）
所有断言类都必须实现的接口 http_assert()"""
class DataAssert(ABC):
    """
    # 抽象基类需要使用内置的abc模块
    # 使用abstractmethod装饰的方法叫做抽象方法
    # 抽象方法子类必须去实现，如果不去实现，实例化的时候报错 TypeError
    """
    @abstractmethod
    def http_assert(self, case, res):
        pass

"""子类继承并实现方法（多态核心）
两个子类方法名完全一样（都是http_assert(case, res)），但内部实现不同"""
class SingleAssert(DataAssert):
    @allure.step("3.HTTP响应断言")
    def http_assert(self, case, res):
        # 在响应断言中判断case[“check”]是否存在 不存在就判断expect是否在res.text里面
        # 存在就使用二次封装的jsonpath把res.json(responsed变成dict)和check传入 提取res里面的目标字段
        if case["check"]:
            # result = jsonpath.jsonpath(res.json(), case["check"])[0]
            # 状态码：200 404 302 500 502
            # 部分接口：重定向  302
            result = GetKeywords.get_keyword(res, case["check"])
            logging.info(f"3.HTTP响应断言内容: 实际结果({result}) ?== 预期结果({case['expected']})")
            assert result == case["expected"]
        else:
            logging.info(f"3.HTTP响应断言内容: 预期结果({case['expected']}) ?in 实际结果({res.text})")
            # 因为返回的res现在是一个字典，没有text的方法
            # 因此这里把返回的字典转成字符串类型，进行断言判断
            # assert case["expected"] in res.text
            assert case["expected"] in str(res)
"""循环检查多个字段"""
class MultipleAssert(DataAssert):
    @allure.step("3.HTTP多重响应断言")
    def http_assert(self, case, res):
        if case["check"]:
            MainAsserts(case, res).main_assert()

def jdbc_assert(case):
    """
    jdbc真正的断言逻辑
    :param case: 测试用例
    :return:
    """
    obj_jdbc_processor(case).jdbc_assert(case)

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
                logging.info(f"3.JDBC响应断言内容: 实际结果(预期结果({case['sql_expected']} ?in {result})")
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
            """
            在Allure报告中添加一个步骤标记，标明这部分代码是“多重数据库断言”的内容。
            •	代码块开始时，Allure会在报告里记录“进入这个步骤”；
	        •	代码块结束时，Allure会在报告里记录“退出这个步骤”；
	        •	如果中间代码抛异常或断言失败，也会在报告中标注异常位置。"""
            with allure.step("3.JDBC多重响应断言"):
                sql_check = eval(case["sql_check"])
                sql_expected = eval(case["sql_expected"])
                for sql, expected in zip(sql_check, sql_expected):
                    result = send_jdbc_request(sql)
                    logging.info(f"3.JDBC多重响应断言内容: 实际结果(预期结果({expected} ?in {result})")
                    pytest.assume(expected in str(result))





