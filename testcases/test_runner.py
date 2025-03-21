import logging

import pytest
from jinja2 import Template
from utils.allure_utils import allure_init
from utils.analyse_case import analyse_case
from utils.asserts import http_assert, jdbc_assert
from utils.excel_utils import read_excel
from utils.extractor import json_extractor, jdbc_extractor
from utils.send_request import send_http_request


class TestRunner:

    # 读测试用例文件中的全部数据, 用属性保存即可
    data = read_excel()

    # 提取后的数据需要初始化一个全局的属性来保存, 可以使用 {} 空字典
    all = {}

    @pytest.mark.parametrize("case", data)
    def test_case(self, case):
        # 引用全局的all (建立测试函数内外 all 变量的对应关系)
        """
        让 all 这个局部变量指向 self.all(函数外的类属性) 这个字典的引用
            如果 self.all 访问的实例属性不存在，就会访问 TestRunner.all（类属性）
            self.all = {"user_id": "1001"}  # 这样就变成实例属性
            print(self.all)  # 访问的是实例属性，不再访问类属性
        """
        all = self.all

        # 根据 all 的值, 渲染case
        """
        ✅ 渲染测试用例 如果 case 里有 ${变量}，会替换成 all 里的值。
        Template(str(case)).render(all)使用 jinja2 进行模板渲染，替换case里${变量}的占位符
        case={"headers": {"Authorization": "Bearer {{token}}"}}
        all = {"token": "abcd1234", "user_id": "1001"}
        -case{"headers": {"Authorization": "Bearer abcd1234"}}
        eval让case从 str - dict
          eval() 本质： 执行字符串形式的 Python 表达式(str像什么)，并返回结果
            如果字符串像 字典 → 解析成 dict
            如果字符串像 列表 → 解析成 list
            如果字符串像 数学表达式 → 计算结果
            如果字符串像 函数调用 → 执行函数
            只能执行单行表达式 不能赋值 导入
        """
        # print("\nstr(case)=",str(case),type(str(case)))
        case = eval(Template(str(case)).render(all))

        # 初始化allure报告
        allure_init(case)

        # 0.测试用例的描述信息日志
        logging.info(f"0.用例ID:{case["id"]} 模块:{case["feature"]} 场景:{case["story"]} 标题:{case["title"]}")

        # 核心步骤1: 解析请求数据
        request_data = analyse_case(case)

        # 核心步骤2: 发起请求, 得到响应结果
        """res 是 requests.Response 对象"""
        res = send_http_request(**request_data)
        print("\n响应的数据结构为：",type(res))
        # 核心步骤3: 处理断言
        # HTTP响应断言
        http_assert(case, res)

        # 数据库断言
        jdbc_assert(case)

        # 核心步骤4: 提取
        # JSON提取
        json_extractor(case, all, res)

        # 数据库提取
        jdbc_extractor(case, all)
