# 这里面存放所有自定义的异常类
class DatabaseException(Exception):
    def __init__(self,message="数据库连接异常，请检查数据库是否启动"):
        # super 表示调用父类的方法
        # 表示父类需要进行正确的初始化
        super().__init__(message,-1)

class GetDataException(Exception):
    def __init__(self,message="数据库查询异常，请检查查询语句的表，字段是否存在"):
        # super 表示调用父类的方法
        # 表示父类需要进行正确的初始化
        super().__init__(message,-1)

class ExecuteSqlException(Exception):
    def __init__(self,message="数据库修改，删除异常，请检查sql语句的表"):
        # super 表示调用父类的方法
        # 表示父类需要进行正确的初始化
        super().__init__(message,-1)