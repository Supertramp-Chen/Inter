import allure

"""
📂 登录模块
    ├── 🔸 验证码场景
    │      ├── ✅ ID:1 -- 成功获取验证码
    │      ├── ❌ ID:2 -- 验证码错误
    ├── 🔸 账号密码场景
    │      ├── ✅ ID:3 -- 登录成功
    │      ├── ❌ ID:4 -- 登录失败

📂 未分类的测试
    ├── ✅ test_case (case1)
    ├── ❌ test_case (case2)
    ├── ✅ test_case (case3)
    ├── ❌ test_case (case4)
    """
def allure_init(case):
    allure.dynamic.feature(case["feature"])
    """ 
    ✅ 给测试用例设置 “场景 (Story)”
    📌 在 Allure 报告里显示 Story: 验证码
    """
    allure.dynamic.story(case["story"])
    # allure.dynamic.title(case["title"])
    allure.dynamic.title(f"ID:{case["id"]} -- {case["title"]}")