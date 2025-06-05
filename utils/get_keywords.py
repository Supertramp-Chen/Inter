# -*- coding:utf-8 -*-

# 面向对象的方式来进行封装
import jsonpath
import logging
"""json断言我二次封装了jsonpath
jsonpath二次封装让excel里的expect不用写$..code 
通过jsonpath.jsonpath(case,f"$..{name}")
            f"$..{name}" 被f-string解析成 "$..code" 查询code字段 返回list
            $  → 代表 JSON 根节点（从 JSON 最外层开始）
	        .. → 代表搜索 JSON 的所有层级（无论 name 处于 JSON 结构的哪个层级）
然后使用try expect
如果jsonpath没有找到 则抓取异常把result=false 
判断result的值为false的话输出查找失败"""
class GetKeywords(object):
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
            # print("date=",data)
            # print("date-type=",type(data))
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