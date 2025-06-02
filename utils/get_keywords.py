# -*- coding:utf-8 -*-

# 面向对象的方式来进行封装
import jsonpath
import logging
"""json断言我二次封装了jsonpath，用了try来抓取异常 如果没有在响应数据里面没有找到
  （jsonpath二次封装：在响应断言中判断case[“check”]是否存在 不存在就判断expect是否在res.text里面，
   存在就使用二次封装的jsonpath把res.json(responsed变成dict)和check传入 提取res里面的目标字段
jsonpath二次封装让excel里的expect不用写$..code 通过jsonpath.jsonpath(case,f"$..{name}")
	然后使用try expect如果jsonpath没有找到抓取异常把result=false 判断result的值为false的话输出查找失败）"""
class GetKeywords(object):
    """
    我们要去实现对jsonpath的二次封装
    通过jsonpath来获取返回值
    """

    @staticmethod
    def get_keyword(data,name,index=0):
        """
        获取json数据里面的一个数据
        :param data: 元数据
        :param name: 需要提取的名称
        :param index: 索引，默认是0
        :return: 最终提取的数据
        """
        try:
            """name=Excel里面的code"""
            print("date=",data)
            print("date-type=",type(data))
            """
            f"$..{name}" 先被 f-string 解析成 "$..code"，即查询 code 字段
            $  → 代表 JSON 根节点（从 JSON 最外层开始）
	        .. → 代表搜索 JSON 的所有层级（无论 name 处于 JSON 结构的哪个层级）
	        {name} → code，即你想要提取的字段
	        jsonpath.jsonpath() 返回所有匹配项
	        返回 list"""
            result = jsonpath.jsonpath(data,f"$..{name}")[index]
        except Exception as e:
            result =  False
        if result is False:
            logging.error(f"jsonpath提取失败: 原本提取的元数据是{data}，提取的值是{name}")
        else:
            return result

    @staticmethod
    def get_keywords(data, name):
        """
        获取提取的多个数据
        :param data: 元数据
        :param name: 需要提取的名称
        :return: 提取出来的数据列表
        """
        try:
            result = jsonpath.jsonpath(data, f"$..{name}")
        except Exception as e:
            result = False
        if result is False:
            logging.error(f"jsonpath提取失败: 原本提取的元数据是{data}，提取的值是{name}")
        else:
            return result