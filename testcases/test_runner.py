import logging

import pytest
from jinja2 import Template
from utils.allure_utils import allure_init
from utils.analyse_case import analyse_case
from utils.asserts import http_assert, jdbc_assert
from utils.excel_utils import read_excel
from utils.extractor import json_extractor, jdbc_extractor,re_extractor
from utils.send_request import send_http_request
class TestRunner:
    """"""
    """
    第二阶段：收集测试用例
    这时候会加载测试类 从而自动加载类属性 执行read_excel函数
    从excel里面读取数据存到字典列表里面(用属性保存) 并通过pytest.mark.parametrise生成全部的测试用例
        (定义两个类属性data列表=read_excel和all空字典
        pytest.mark.parametrize里写上类属性data
        pytest.mark.parametrize会遍历data 把字典列表里的每一个字典作为一个测试用例的数据 生成全部的测试用例)
    """
    """
    类属性 定义在类的外层 属于类本身 所有对象共享 共用一份数据
        在类加载时就会被执行并赋值 ，类定义时就被创建
        每次运行 pytest 时，都会重新加载测试类文件并重新赋值类属性
    实例属性 定义在方法中 属于某个对象 不共享
        创建实例时赋值
    如果在实例中定义了一个和类属性同名的属性，实例的这个属性会遮蔽掉类属性，访问时会优先使用实例属性
    """
    data = read_excel()
    all = {} # 把提取后的数据保存于 全局的属性 空字典
    @pytest.mark.parametrize("case", data)
    def test_case(self, case):
        """"""
        """第四阶段：执行测试用例
        建立测试函数内外all变量的对应关系，局部变量all指向 函数外 类属性self.all字典的引用
        
        首先使用jinjia2模块进行渲染测试用例 把其中{{}}的变量替换成all里面对应的值
	        （数据依赖处理：先通过json提取数据到all里面 渲染 然后用eval转化成字典）
	    
	    allure二次封装：通过allure.dynamic.feature/title(case[“feature”]) 让allure报告可以按照feature story分类 
		    以及在步骤之前使用@allure.step在allure报告添加测试步骤 以及使用allure.attach在具体步骤里添加附件）
        
        然后解析请求数据 把测试用例case字典里面键值对的value用eval从str变成字典 request能发送的格式(headers params data json file)
		    组装并返回request需要的请求数据 method url headers params data json file
		    
		然后用request方法发送http请求 传入解析出来的数据 返回一个response对象，并且封装到工具类 ; jdbc请求
		（请求封装：先解析字典case中的请求字段 使用eval把字典里面headers params data json的value转化成字典 
		
		然后发送http请求 使用字典解包 
		**requesdata 展开字典的key value去掉key的引号变成key=value的形式 作为参数传给函数 
		用requests.request发送http请求 返还一个response对象res
		
		
        然后进行断言
        json断言我二次封装了jsonpath，用了try来抓取异常 如果没有在响应数据里面没有找到
	        （jsonpath二次封装：在响应断言中判断case[“check”]是否存在 不存在就判断expect是否在res.text里面，
	        存在就使用二次封装的jsonpath把res.json(responsed变成dict)和check传入 提取res里面的目标字段
		jsonpath二次封装让excel里的expect不用写$..code 通过jsonpath.jsonpath(case,f"$..{name}")
		然后使用try expect如果jsonpath没有找到抓取异常把result=false 判断result的值为false的话输出查找失败）
        
        数据库断言就是创建数据库连接 创建游标 执行sql
        
    提取分为数据库提取和json提取
    我还写了验证码识别的工具类，验证码一般都是base64，我先把他用，分割得到后面的编码部分，用pil模块转化成图片数据 然后用dddocr进行识别
			(接口自动化中日志处理模块
				在pytest.ini里配置log保存路径(log_file=) 级别(log_file_level=info) 格式 (log_file_format)
				测试函数里使用logging.info()
			接口自动化中ORC识别
				验证码图片通常是 Base64 编码
				先从逗号分割保留 Base64编码部分 
				解码然后用pil转化为图片格式 
				然后用ddddocr进行orc识别 提取验证码字符
			接口自动化中数据库连接)"""
        # print("case=", case, "\ntype-case=", type(case))
        """
        建立测试函数内外all变量的对应关系，局部变量all指向 函数外 类属性self.all字典的引用
            如果在实例中赋值 self.all 其会生成实例属性 并遮蔽掉类属性all 访问self.all是访问实例属性
                self.all = {"user_id": "1001"}  # 这样就变成实例属性
                print(self.all)  # 访问的是实例属性，不再访问类属性
        """
        all = self.all
        """
        ✅ 渲染测试用例 如果 case 里有 {{变量}}，会替换成 all 里的值
        Template(str(case)).render(all) 替换case里{{变量}}的占位符
            case = {'json': '{"uuid":"{{uuid}}","code":"2"}'}
            all = {'uuid': 'e4d21f5e3a93441da4c76428c97e937c'}
            case = '{"uuid":"e4d21f5e3a93441da4c76428c97e937c"}'
        eval让case从 str - dict (因为渲染的时候把case变成str了)
          eval() 本质： 执行str字符串形式的Python表达式(str像什么)，并返回结果
            如果字符串像 字典 → 解析成 dict
            如果字符串像 列表 → 解析成 list
	        如果字符串像 数学表达式 → 计算结果
	        如果字符串像 函数调用 → 执行函数
	        只能执行单行表达式 不能赋值 导入
        """
        case = eval(Template(str(case)).render(all))
        # print("case2=", case, "\ntype-case2=", type(case))
        # 初始化allure报告
        """让allure报告有清晰的分组"""
        allure_init(case)
        """
        ✅ pytest 在终端输出测试用例信息。
        打印测试用例的信息到日志（log 文件）和终端，方便调试和分析测试过程。
         f"..." 是 Python 的 格式化字符串（f-string）
         f 会把 case 里的值填充进去
         INFO -- 0.用例ID:1 模块:登录 场景:验证码 标题:成功获取验证码
	    """
        # 0.测试用例的描述信息日志
        logging.info(f"0.用例ID:{case['id']} 模块:{case['feature']} 场景:{case['story']} 标题:{case['title']}")
        """
        ✅ 解析 提取 API 请求数据"""
        request_data = analyse_case(case)
        """
        ✅ 用 requests 发送 API 请求，并获取 HTTP 响应。"""
        res = send_http_request(**request_data)
        # 核心步骤3: 处理断言
        """
        ✅ 响应断言 检查 response.status_code 和 response.json() 是否符合预期"""
        http_assert(case, res)
        # HTTP响应断言
        # try:
        #     # 可能出现异常的代码
        #     eval(case["check"])
        # except:
        #     # 出现异常之后，表示断言不是字典，因此走老逻辑
        #     http_assert(case, res)
        # else:
        #     # 没有出现异常，表示可以转成字典，走多重断言的逻辑
        #     http_asserts(case, res)

        # 数据库断言
        # try:
        #     eval(case["sql_check"])
        # except:
        #     jdbc_assert(case)
        # else:
        #     jdbc_asserts(case)
        """
        ✅ SQL断言 执行 SQL 查询，检查数据库里是否有对应数据。"""
        jdbc_assert(case)

        # 核心步骤4: 提取
        """
        json_extractor、jdbc_extractor 和 re_extractor 
        负责 从接口返回的数据或数据库结果中提取信息 并存入 all
        """
        # JSON提取
        """
        ✅ 提取 response.json() 里的 token, order_id 并存入 all。"""
        json_extractor(case, all, res)

        # 数据库提取
        """
        ✅ 提取数据库查询结果中的 user_id。"""
        jdbc_extractor(case, all)
        # 正则提取
        """
        ✅ 用正则提取 验证码, 订单号 等信息。"""
        re_extractor(case, all, res)
