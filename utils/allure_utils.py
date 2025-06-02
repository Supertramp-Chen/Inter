import allure

"""
allure报告的功能模块
📂 feature模块
    ├── 🔸 story场景
    │      ├── ✅ title标题
    │      ├── ❌ ID:2 -- 验证码错误
    ├── 🔸 story场景
    │      ├── ✅ ID:3 -- 登录成功
    │      ├── ❌ ID:4 -- 登录失败
    """
"""
allure报告中的自定义属性：
feature用于标记测试用例的 模块名 
story用于标记测试用例的 场景名 
title用于标记测试用例的 标题 
description描述 
issue集成bug系统，可填入bug链接"""
def allure_init(case):
    allure.dynamic.feature(case["feature"])
    allure.dynamic.story(case["story"])
    # allure.dynamic.title(case["title"])
    allure.dynamic.title(f"ID:{case['id']} -- {case['title']}")