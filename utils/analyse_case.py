import logging
import allure
# from numpy.distutils.conv_template import header
from config.config import BASE_URL
from utils.data_preprocessor import *

"""
API 请求的数据 能在日志和 Allure 报告里清晰展示
analyse_case(case) 解析测试用例中的请求数据，并转换成 requests 能直接发送的格式 字典
    将字符串类型的字段 转换为 Python 数据类型（使用 eval()）
    记录日志，方便调试请求数据，在 Allure 报告中添加测试步骤信息。
"""
"""在Allure 报告中添加“解析请求数据”步骤"""
@allure.step("1.解析请求数据")
def analyse_case(case):
    # print("case3=", case["method"], "\ntype-case3=", type(case))
    method = case["method"]
    url = BASE_URL + case["path"]
    """
    首先判断是不是字符串
        如果 case["headers"] 是字符串，就用 eval() 转换成 Python 数据类型
	    如果 case["headers"] 不是字符串，直接赋值 None
	"""
    hearders = eval(case["headers"]) if isinstance(case["headers"], str) else None
    params = eval(case["params"]) if isinstance(case["params"], str) else None
    data = eval(case["data"]) if isinstance(case["data"], str) else None
    json = eval(case["json"]) if isinstance(case["json"], str) else None
    files = eval(case["files"]) if isinstance(case["files"], str) else None
    """组装request需要的请求数据"""
    request_data = {
        "method": method,
        "url": url,
        "headers": hearders,
        "params": params,
        "data": data,
        "json": json,
        "files": files,
    }
    # print("request_data=", request_data, "\ntype-request_data=", type(request_data))
    """
    日志里记录请求数据
    	•	在终端和日志文件里记录解析的请求数据
	    •	如果请求失败，可以检查日志，看看数据是否正确
	allure报告添加数据
		•	在 Allure 测试报告里，记录解析后的请求数据
	    •	Allure 报告里会有一个附件，展示请求数据
	"""
    logging.info(f"1.解析请求数据, 请求数据为: {request_data}")
    allure.attach(f"{request_data}", name="解析数据结果")
    return request_data