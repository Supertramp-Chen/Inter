# 3️⃣ **自动化 接口—流程 原理** 🧠

# 一、接口测试

# 一言蔽之

设参数、发请求、解析响应、断言



**主要根据api文档进行测试 使用jemter进行测试**



**http状态码 请求内容 常见请求方式 请求头响应头的字段 一个接口对应的用例** 

**线程组中 线程数 启动时间 循环次数 对称加密 sign 接口测试业务场景**

**http https session cookie token get post 定位bug 连数据库 接口幂等性 接口越权 依赖第三方接口 多接口 jemter常用函数** 



## 接口功能测试开展

开发编码阶段 开发写好一个接口就测一个 测试左移,提前找出较深层的后端bug,减少系统测试时bug数

根据API文档进行测试(接口业务,地址,请求方式,入参,出参,鉴权方式) 

设计接口功能测试用例(正向+逆向) 然后用例评审

用Jmeter写脚本 进行测试 产出测试报告

​	接口功能测试：100%覆盖,正向+逆向用例,不需要重复执行 (除非有些大额支付的场景，我们没有覆盖到之外)

​	接口回归测试：自动化,覆盖重要+使用频率高,1条正向用例,重复执行

用例：

(业务逻辑)如果关联上下游模块的其他接口 验证接口调用是否成功，整体数据规则是否正确 如是否存在唯一性问题和其他的数据逻辑

(字段校验)对请求中的每个参数做字段校验,遍历字段的类型/长度/必填/唯一的组合

(异常)在弱网和断网状态下请求，观察结构是否符合预期

(权限)在有无权限下验证接口请求是否成功,响应结果是否正确

(安全)测试接口是否存在越权的bug,另外在文件上传类的接口上也要额外注意安全性,比如文件格式，大小,文件服务器地址等,要尽可能保证安全



## 接口本质

​	能被前端访问的后端的函数

​	http接口 tcp接口 socket接口 webservice接口 restful规范

请求行：请求方式 + URL(url后面的url参数params) — GET /xxx?key=value

​				查get 增post 改put 删delete

​				URL - 协议 ip 端口 路径

请求头：支持语言，浏览器信息 — Content-Type: application/json

请求体：请求参数(data json) — key=value&key2=value2 | {“key": "value"}



响应行：http协议版本，状态码

响应头：web服务器信息，响应内容的类型，响应内容的长度

响应体：http响应的具体数据





提交方式不同，get提交的数据显示在地址栏，post是隐式的提交数据，后者更安全

可提交的数据量不同，get提交的数据量有限制，而post无限制

执行效率不同，get的执行效率比post稍高



1.首先新建一个线程组

2.然后新建一个HTTP请求默认值(输入服务器的IP和端口)

3.再创建HTTP请求,一个取样器对应一个接口,输入路径,请求方式,请求参数

4.然后创建断言和查看结果数

调试和执行用例过程中:

比如参数化,一般指的是测试同一个接口时,可以由多组测试数据产生不同的响应结果，我会使用参数化,用csv文件来保存测试数据,用jmeter的csv数据文件设置来逐行读取测试数据，断言的数据也可以一起保存在csv文件中

比如关联,一般指的是上下游接口之间存在数据依赖,我会先请求上游接口,在jmeter中通过json提取器根据jsonpath来提取数据,并在下游接口请求时引用即可,如果涉及跨线程组关联,就需要先在beanshell中执行setproperty函数来实现把提取的数据导出为全局属性再通过property函数进行引用

比如鉴权,和关联是一样的,只不过上游接口是登录,需要提取的数据是登录得到的token,然后我们在其他接口的请求中引用token即可

比如数据需要加解密的情况,如果是简单的md5加密,可以直接通过jmeter的内置函数实现,如果是复杂的加解密方式，可以直接和开发拿对应的代码,在jmeter的beanshell中调用对数据进行处理即可



o bug

比如文件上传,和普通的请求一样,在jmeter的http请求组件中有个选项卡专门用于文件上传传参,写好文件路径,参数名称和MIME类型后就可以实现文件上传了

在数据唯一性校验上的bug,也可以叫幂等性方面的bug(WMS项目中出现过)

当时新增入库单时,是存在唯一校验的,根据入库单号来判断入库单的唯一性,但是从接口做并发测试，就发现这个唯一校验会失效,后来排查原因发现,后端实现唯一校验的逻辑就是看数据库里有没有同入库单号的数据，因为并发会导致来不及判断,所以出现了这个的bug,后面后端修复的时候是给数据库做了加锁的操作,确保其他请求不能同时操作入库数据表,就解决了这个bug



​	根据API文档，接口功能：每个接口设计正向 逆向原理，jmeter脚本执行；接口回归：覆盖重要的接口 不用100% 一条正向用例 重复执行

​	测试左移 提前找出bug开发写一个测一个



具体操作

​	jmeter创建 线程组 http请求默认值 http请求 断言 查看结果树

​	参数化：

​	关联

​	鉴权

​	加解密



jmeter连接数据库

下载数据库驱动 jemter数据库连接里配置数据库信息



软件测试面试题：下个接口用到上个接口的数

据，但返回的数据加密了，怎么提取？

回答：

比如：一次登录后做多个接口的操作，然后登录后的uid需要关联传递给

其他接口发送请求的时候使用。

首先会让开发写一个加解密的jar包，然后把jar包放入到jmeter的lib/

ext目录下。

然后在测试计划中有一个add Directoryorjarto classpath，在这里

指定jar的路径，添加需要的jar包。

在第一个接口中添加一个bean shellpostprocessor（后置处理器），在

后置处理器中编写java代码。

具体如下：

导入解密的jar包中的解密算法类；

导入用于解析json格式数据的类（假设返回的数据是json格式的）对数据

进行处理器；

首先获取接口的返回数据，然后调用解密算法类中的函数进行解密解

密出来后就是一个ison格式数据；

然后调用json库中的函数对json数据进行解释，提取截取响应信息中

uid的值将uid str数据存到变量中，这里用props.put，其他线程组可

调用请该变量。



## jmeter执行顺序

1）配置元件（configelements）：http请求默认值、信息头管理器、JDBc配置

特点：配置初始化数据

2）前置处理器（Pre-processors)：用户参数

特点：设置取样器执行所需数据

3）定时器（timers）：常量吞吐定时器、同步定时器

特点：设置取样器的执行规则

4）取样器(Sampler)：http请求、JDBC Request

特点：核心



5）后置处理程序（Post-processors)：JSoN提取器

特点：从响应结果提取数据

6）断言(Assertions)：响应断言

特点：判断响应结果

7）监听器（Listeners)：查看结果树、聚合报告

特点：显示最终的运行结果



# 

# 一言蔽之

==亮点：0-1搭建框架➕钉钉集成==

定位 断言 —— 封装框架和工具类 —— 高级语法 优化框架结构 —— 用源码逻辑 优化框架运算时间,代码结构,执行效率,内存管理,垃圾回收

**命令行输入pytest后：

**API：**

- [ ] 第一阶段 解析pytest.ini文件：配置默认参数 输出日志

- [ ] 第二阶段 收集测试用例 这时候会加载测试类                                                                         从而自动加载类属性data*列表*=read_excel和all空字典 执行read_excel函数                                                    从excel里面读取数据存到字典列表里面*(*用属性保存)                                                             pytest.mark.parametrise("case", data)把字典列表里的每一个字典作为一个测试用例的数据 生成测试用例 


```apl
类属性： 定义在类的外层 属于类本身 类定义时就被创建 所有对象共享 共用一份数据
在类加载时就会被执行并赋值，每次运行 pytest 时，都会重新加载测试类文件并重新赋值类属性
实例属性 定义在方法中 属于某个对象 不共享
创建实例时赋值
如果在实例中定义了一个和类属性同名的属性，实例的这个属性会遮蔽掉类属性，访问时会优先使用实例属性)
```

```apl
读取excel：使用*openpyxl*库里的方法加载*excel* 并且选择*excel*里的表 
然后读取excel*第二行的关键字数据存到*list* 
然后遍历excel*第三行开始的数据读取到元组*tuple*
用zip函数把他们两个转化成键值对
用dict把它变成字典
最后判断其中的istrue关键字是*true*的话就添加到字典列表*data*里面
关闭文件 返回字典列表data
```

- [ ] 第三阶段 解析pytest.fixture装饰器 执行前置操作 按scope顺序session model class function

​	conftest里用fixture+生成器 编写数据清除函数 实现测试用例执行完后自动清除数据

```apl
	pymysql二次封装

		连接数据库 执行sql

		conn=pymysql.Connect(参数)创建数据库连接 

		cur=conn.cursor()创建游标 

		写个for循环执行sql cur.execute()

		关闭连接和游标
```

- [ ] 第四阶段 执行测试用例

   建立测试函数内外all变量的对应关系，局部变量all指向函数外类属性self.all字典的引用

   首先使用jinjia2模块进行渲染测试用例 把其中{{}}的变量替换成all里面对应的值

​    （数据依赖处理：先通过json提取数据到all里面 渲染 然后用eval转化成字典）

​	allure二次封装：通过allure.dynamic.feature/title(case[“feature”]) 让allure报告可以按照feature story分类；以及在步骤之前使用@allure.step在allure报告添加测试步骤 以及使用allure.attach在具体步骤里添加附件）

然后解析请求数据 把测试用例case字典里面键值对的value用eval从str变成字典 request能发送的格式

​	(headers params data json file)

组装并返回request需要的请求数据 method url headers params data json file

​	然后用request方法发送http请求 传入解析出来的数据 返回一个response对象，并且封装到工具类 ; jdbc请求

​	（请求封装：先解析字典case中的请求字段 使用eval把字典里面headers params data json的value转化成字典 

​	然后发送http请求 使用字典解包 

​	字典解包 requesdata 展开字典的key value去掉key的引号变成key=value的形式 作为参数传给函数 

​	用requests.request发送http请求 返还一个response对象res

```
自定义异常：更清晰地标识出错的原因（比如连接失败、查询失败等）
jsonpath二次封装
接口响应添加状态码和响应时间
pymysql封装
私有属性 私有方法的应用
pytest-assume
封装 继承思想实现多重断言 字符串断言 类型断言 响应时间断言 断言模版
方法重写 抽象基类 多态断言
```



- [ ] 第五阶段 pytest 通过 fixture 机制 测试用例执行完之后自动调用next函数 然后执行yield后面的后置操作

## API数据变化

### read_excel

```apl
keys= 
[
'id', 'feature', 'story', 'title', 'method', 'path', 'headers', 'params', 'data', 'json', 'files', 'check', 'expected', 'sql_check', 'sql_expected', 'jsonExData', 'sqlExData', 'reExData', 'is_true'
] 
row= 
(
1, '登录', '获取验证码', '成功获取验证码', 'get', '/captchaImage', None, None, None, None, None, 'code', 200, None, None, '{"uuid":"uuid"}', None, None, True
) 
dict_data= 
{
'id': 1, 'feature': '登录', 'story': '获取验证码', 'title': '成功获取验证码', 'method': 'get', 'path': '/captchaImage', 'headers': None, 'params': None, 'data': None, 'json': None, 'files': None, 'check': 'code', 'expected': 200, 'sql_check': None, 'sql_expected': None, 'jsonExData': '{"uuid":"uuid"}', 'sqlExData': None, 'reExData': None, 'is_true': True
} 
遍历：row -dict_data -data
data= 
[
    {'id': 1, 'feature': '登录', 'story': '获取验证码', 'title': '成功获取验证码', 'method': 'get', 'path': '/captchaImage', 
'headers': None, 'params': None, 'data': None, 'json': None, 'files': None, 'check': 'code', 'expected': 200, 'sql_check': None, 'sql_expected': None, 'jsonExData': '{"uuid":"uuid"}', 'sqlExData': None, 'reExData': None, 'is_true': True}, 

    {'id': 2, 'feature': '登录', 'story': '登录', 'title': '正常登录获取token', 'method': 'post', 'path': '/login', 
'headers': '{"content-type":"application/json;charset=UTF-8"}', 'params': None, 'data': None, 'json': '{"password":"e10adc3949ba59abbe56e057f20f883e","username":"admin","uuid":"{{uuid}}","code":"2"}', 'files': None, 'check': 'code', 'expected': 200, 'sql_check': None, 'sql_expected': None, 'jsonExData': '{"token":"token"}', 'sqlExData': None, 'reExData': None, 'is_true': True}
] 
```

### test_case

```apl
case= 
{
'id': 1, 'feature': '登录', 'story': '获取验证码', 'title': '成功获取验证码', 'method': 'get', 'path': '/captchaImage', 'headers': None, 'params': None, 'data': None, 'json': None, 'files': None, 'check': 'code', 'expected': 200, 'sql_check': None, 'sql_expected': None, 'jsonExData': '{"uuid":"uuid"}', 'sqlExData': None, 'reExData': None, 'is_true': True
} 
type-case= <class 'dict'>
case= 
{
'id': 1, 'feature': '登录', 'story': '获取验证码', 'title': '成功获取验证码', 'method': 'get', 'path': '/captchaImage', 'headers': None, 'params': None, 'data': None, 'json': None, 'files': None, 'check': 'code', 'expected': 200, 'sql_check': None, 'sql_expected': None, 'jsonExData': '{"uuid":"uuid"}', 'sqlExData': None, 'reExData': None, 'is_true': True
} 
type-case= <class 'dict'>
```

### analyse_case

```apl
case= 
{
'id': 2, 'feature': '登录', 'story': '登录', 'title': '正常登录获取token', 
'method': 'post ,
'path':'/login', 
'headers': '{"content-type":"application/json;charset=UTF-8"}', 
'params': None, 
'data': None, 
'json': '{"password":"e10adc3949ba59abbe56e057f20f883e",
"username":"admin","uuid":"6421860e6b5848ecb6ea5170257fc923","code":"2"}', 
'files': None, 
'check': 'code', 'expected': 200, 'sql_check': None, 'sql_expected': None, 'jsonExData': '{"token":"token"}', 'sqlExData': None, 'reExData': None, 'is_true': True
}'
request_data= 
{
'method': 'post', 
'url': 'http://60.204.225.104:9632/login', 
'headers': {'content-type': 'application/json;charset=UTF-8'}, 
'params': None,
'data': None, 
'json': 
, 
'files': None
} 
```

### send_http_request

```apl
# 字典 -关键字参数 -Response对象
requests.request(
    method="post",
    url="http://60.204.225.104:9632/login",
    headers={"content-type": "application/json;charset=UTF-8"},
    json={
        "password": "e10adc3949ba59abbe56e057f20f883e",
        "username": "admin",
        "uuid": "15164c400d954da699a7baa9777c15e2",
        "code": "2"
    }
)
type-res= <class 'requests.models.Response'> 
```

### http_assert

```apl
# response对象 -JSON 解析为dict  
res= {
'msg': '操作成功', 
'img': '/9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAA8AKADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDtrW1ga1hZoIySikkoOeKsCztv+feL/vgU2z/484P+ua/yqyKiMY8q0IjGPKtCIWdr/wA+0P8A3wKeLK1/59of+/YqUU4U+WPYfLHsRCytP+fWH/v2KcLG0/59YP8Av2KmFOBFHLHsHLHsRCws/wDn1g/79inCws/+fSD/AL9iphTxRyx7Byx7EI0+y/59Lf8A79j/AApw06y/587f/v0v+FTis7Wtf0/w9p73uoTeXEpwABlmPoB3NXCjzyUIRu30sDjFdC6NOsf+fO3/AO/S/wCFOGm2P/Plb/8Afpf8KzPDXiey8UWDXtlHPHEHKYmUAnHcYJrdFOrQdKbhONmt0CjF6pFcaZYf8+Vt/wB+l/wp40yw/wCfG2/79L/hVjOK5DxH8SdE8M6kLC7FxJcBQzrEmQoPTkkc1VDCTxE/Z0Ycz7JCaitWdSNL0/8A58bb/vyv+FPGlaf/AM+Fr/35X/Cs7w/4q0jxLbedpl2suPvRn5XT6qef6VuLzUVKLpycJxs10aGoxeyKw0rTv+fC1/78r/hThpOnf9A+1/78r/hVoU8VHLHsHLHsVRpOm/8AQPtP+/K/4VW1PS9Pj0i9dLG1V1gcqwhUEHaeRxWsKq6t/wAgW/8A+veT/wBBNKUY8r0FKMeV6HJWf/HnB/1zX+VWRVez/wCPOD/rmv8AKrIpx+FDj8KHCndBSClYZWqKOD+IPiPWtFto5NNEfkNxJJjLIe3Hp715hZeK9at9Ytru71G8aEyq7oZWCMM8/LnBr2DxHpkl3E6gZUjBHrXl+teHJvJKqmGTlP8ACvpcozTCUYLD16S952cutn/l+RjUhJ6pnultqEVxapOjAoygg+1cNoPjLVIvH97oGsXCSwMz/ZXMaqf7yjIAzlc/jXEaL4hv7vw9JoUd9JaXkJzBJnbuUdUJ6j8PQe9Yl5a61DeJeSXL3FxCQyzCQuy4OR154Na4bKaNGpVw+JqRTatG+/eMk9rPbcTqNpOKPpl5gsRbPavn/wAbazd+KNavCC6WdgCIo27nPJx6nn8q6Wz+L1q2niO/sLgXAXBMJVlY+vJBH05p0sMHiLT11OzGUmHII5BHUH3FclCGKyabr1aOuyb2T6/erlNxqaJlf4X+JItO0e+hmDstsTMVjGWKdyB3xzXrWkeI9I1q3E2n6hBcKRkhWwy/VTyPxFfOjfavCWvR3kIPlEkY7Ed1Nal5onh28jjvYrv7FHN8wBI259BnGPpXbmGDwmJq/WuZqNXVNLms+sWt7/8AB7EwlJLl7Huc/inRV1OLS11K3a+myEhRtxyATzjgdO9clr2iWU+qz6hNZRzzyqFYyLuGAMYwa8807UvDPhmdJrO1k1XUEOY2Jwqn1B/wzXsOgXv/AAkOgxXlxZyWs7DEkUikYPqM9QfWvKxmDng0qtDmUXpd+636K97epcZKWjPHNZjl8Jatb6xojtakth4lJ2g/T0PPHavevCniCPxFoNpqKDaZUy6f3WHBH514p8ULGaC4iljz9nzhgOx7V3fwmuIj4Zto4XDBSd3s2eRXbj/3+U0cTUfNNNxv1tro337Ex0qNLY9QFPFMTkCpBXzZsOFVdW/5Al//ANe0n/oJq2Kq6v8A8gS//wCvaT/0E1MvhZMvhZyVn/x5Qf8AXNf5VZFV7L/jyg/65r/KrIoj8KCPwocKcBSCniqKGPCsg5Fc/rWjJNExVea6UUkkQkUgigD5+8Q+HruLUFurCNvN3fMq8c/3v8a6Sz0a6udOSe4tzDcY+dcg8+oIrvr3QVml3havWulhIdhFd1fH1K9CFCok+TZ9bdt9vkSoJNtHgt/ZnQdajvTapNbu+HidAwz3wD0PcV7XosEd5pkTIo8tkBQBccEccdqjuvDym53qveuh0218iELijFY6WJp041F70Va9910uu679QjHlbsec+LPDaTQyIyfK3cDofWvNNOZbW7m0XUl3W8jbc/3G7MPrX0fqunLdQMNvOK85vvBVreagHubUPg4yCVP5g105bmUcNCdGtdwlrpvGS2kvMmcL6rcr6D4Yt7OVXtrcbv77cmvUNLtpEtwG9Ki0bTI4bdF2Y2gAZrfjjCjAFeZVqzqyc6km33ZaSWx5/wCLdCF7G6vHvRhgg1w/h3WrfwH4lh0sWNw0V26ebO8hbIPAKoB2J578fSvcby0WeMgiuZ/sUJqKziJfMXIV9vIB6gGujC4pUoyp1E5Ql0u1r0fyFKN9UdnA4dARU4qnYoyxAHrV0VxlDhVXV/8AkCX/AP17Sf8AoJq2Kq6v/wAgS/8A+vaT/wBBNTL4WTL4WclZf8eVv/1zX+VWRXMxa1cxRJGqREIoUZB7fjUn9v3X/POH/vk/41lGtGyM41Y2R0opwrmf+Ehu/wDnnB/3yf8AGl/4SK7/AOecH/fJ/wAar20R+2idQKeK5X/hJLz/AJ5Qf98n/Gl/4SW8/wCeUH/fJ/xo9tEPbROrCg09VArkv+Envf8Anlb/APfLf40v/CUXv/PK3/75b/Gj20Q9tE63yweoqRVArj/+Eqvv+eVv/wB8t/jS/wDCV33/ADytv++W/wAaPbRD20TsioYVAbKNm3bRXK/8Jbf/APPG2/75b/Gl/wCEv1D/AJ423/fLf/FUe2iHtonZxRBBgCphXD/8JhqH/PG1/wC+W/8AiqX/AITLUf8Anja/98t/8VR7aIe2idzjIpPIUnOK4j/hM9R/542v/fDf/FUv/Ca6l/zwtP8Avhv/AIqj20Q9tE7xFCjipBXAf8JtqX/PC0/74b/4ql/4TjU/+eFp/wB8N/8AFUe2iHtonoIqrq//ACA9Q/69pP8A0E1xX/Cc6n/zwtP++G/+KqO58Z6jdWs1u8NqElRkYqrZAIxx81TKtGzFKrGzP//Z', 
'code': 200, 
'captchaOnOff': True, 
'uuid': 'a1d432497a8143c8948e6e3dc0ea4990'
} 
type-res= <class 'dict'>
```



## 自动化开展

当时项目开发迭代了3个月了，总用例数突破1000+，需要回归的测试用例也有近300条

手工回归测试的效率太低,并且项目旧接口比较稳定 适合做接口自动化，页面功能比较稳定 适合做UI自动化

所以用自动化测试框架来提高回归效率

我从0到1搭建了基于KDT的接口自动化框架和基于PO模式的UI自动化框架 并且结合GitHub和Jenkins实现CI流程

- 用python做接口测试和懂一点计算机网络，那么我会找一个我们项目中用的第三方软件的文档，把它的接口鉴权这几行文档抄到题目里。然后让来面试的人讲下用python怎么实现这个接口调用
- 各种鉴权的用法，区别。比如 cookie session 鉴权跟token 鉴权有啥区别，为啥用这种不用那种。但知道放header 其实也够了。
- 实际上我项目里header我都处理好了，我估计一年也不需要他写一次header

## 框架搭建

### API

技术栈：

采用KDT思想,使用python+requests+pymysql+pytest+allure+excel关键字驱动来实现（代码里根据这些关键字字段的值来执行不同的流程）

核心业务流程：

excel测试用例解析->全局变量引用->allure报告初始化 -> 发请求 -> 断言 ->提取 ->生成allure测试报告

目录结构：

testcases 下保存测试脚本；utils 目录用于保存各种工具类或工具函数,如 excel 用例读取,请求数据解析,allure报告初始化,请求,断言,提取器；data 下保存excel测试用例文件；file 目录用于保存待上传的文件；config 目录用于保存项目的基础配置信息,如 base_url,数据库配置；report目录；log目录；此外还有胶水文件,日志配置文件

3框架搭好后,工作主要是丰富接口测试用例,目标是覆盖80%的旧接口

最后结合jenkins做了持续集成,定时检测,只要被测项目的git仓库存在代码更新,就重新部署测试环境并自动运行自动化测试代码，结束后发送测试报告到钉钉群



涉及到的库：time,pytest,openpyxl,requests,selenium,pymysql,jinja2,jsonpath,logging等

























数据驱动

接口自动化里的数据驱动或关键字驱动是什么，怎么实现的?

先说说我对数据驱动的理解,

数据驱动是一种依赖参数化技术的设计思想,规范化测试过程,

让测试数据来决定测试结果，这样就能减少对测试脚本的直接维护



测试脚本的核心逻辑不变，**测试数据变化**，测试结果由数据决定



关键字驱动是在 数据驱动 的基础上,额外增加一系列 步骤或操作有关的关键字数据

在数据驱动基础上，增加了一层**抽象**，即用关键字（Keyword）表示测试步骤，而不是直接在代码里写具体的测试逻辑。

我在框架中的实现是



先定义测试用例的模板数据和业务逻辑 

再通过 openpyxl 封装了从 excel 文件中读数据的工具函数

最后在 测试脚本中进行处理,如模板渲染和请求数据解析等









**元素定位不到的情况有哪些？**	

​	1、文件上传 -第三方库pywinauto定位window系统框 2、悬浮元素 -用debugger固定在页面上再定位 3、动态id -用xpath 4、句柄跳转 -用switch to定位

**高亮元素怎么定位**	

​	(Css的一些背景样式) 用css样式的class选择器定位

**一个元素怎么都定位不到**	

​	pyautogui绝对定位





**UI自动化怎么写？**	

​	1、功能测试用例一步步转化成代码 2、预期结果转化成断言 3、写完提交到git和Jenkins持续集成ci 回归阶段跑一下看有没有bug







**pytest？**

​	Pytest有夹具fixture可以结合装饰器 生成器实现前置处理 后置清除 —————————@pytest.mark.skip()、@pytest.mark.skipif()、@pytest -k “dog”



**PO模式？**	1、PO模式就是把元素和操作分开 2、把页面的结构和功能封装到一个对象里 3、测试用例代码通过操作这些对象和页面交互 而不是直接操作页面的元素



对象库层:封装定位元素的方法O

操作层:封装对元素的操作O

业务层:将一个或多个操作组合起来完成一个业务功能。比如登录:需要输入帐号、密码、点击登录三个操作0



**元素定位不到的情况有哪些？**	

​	1、文件上传 -第三方库pywinauto定位window系统框 2、悬浮元素 -用debugger固定在页面上再定位 3、动态id -用xpath 4、句柄跳转 -用switch to定位



**高亮元素怎么定位**	

​	(Css的一些背景样式) 用css样式的class选择器定位



**一个元素怎么都定位不到**	

​	pyautogui绝对定位



**数据驱动ddt**	

​	把数据放到csv文件 然后写个函数用生成器迭代器一行行读



**失败用例重跑**	

​	pytest.ini文件加上--reruns=2



**让自动化用例跑的更快**	

​	多线程 -pytest-xdist插件 pytest.ini文件用参数-n指定线程数 -一般20线程跑2 3小时



**装饰器**	

​	1、参数是函数 内部还有个函数 返回值是一个函数对象 2、@装饰器函数

修饰函数的函数,不改变原有函数代码的基础上,动态的改变函数的功能

在我的框架中,用装饰器生成器实现全局管理drvier 自动登陆登出



**fixture**	

​	 1、Fixture源码传参有一个是函数 内部还有函数 返回值也是函数对象 2、自动登陆 登出 3、自动传入driver 清理driver 全局管理diver



**自动化bug**	

​	一个表单的电话号码字段 自动化断言失败 看了截图发现框没有数字后面写的11/11 而不是0/11 -清空数字的时候没有动态改变状态



**可迭代对象,迭代器,生成器?**

​	可迭代对象一般是能直接用于 for 循环遍历的数据对象,

​		比如:常见容器类型数据str, list, tuple, set, dict等都是可迭代对象,还有一些函数的返回值如 range() 函数的返回值也是一个迭代的对象

​	迭代器和可迭代对象很像,是可以被 next() 函数调用并不断返回下一个值的对象,但区别是可迭代对象一次性生成全部值,但迭代器每次被 next() 函数调用只生成一个值,不会一次性全部生成

​	生成器是一种特殊的迭代器，	函数有yield的都可以叫生成器 被调用的时候执行到yield就会停止 接收到next函数后才会执行后面的





什么是可迭代对象,迭代器,生成器?

可迭代对象一般是能直接用于 for 循环遍历的数据对象,比如:常见容器类型数据str, list, tuple, set, dict等都是可迭代对象,还有一些函数的返回值如 range() 函数的返回值也是一个迭代的对象迭代器和可迭代对象很像,是可以被 next() 函数调用并不断返回下一个值的对象,但区别是可迭代对象一次性生成全部值,但迭代器每次被 next() 函数调用只生成一个值,不会一次性全部生成生成器是一种特殊的迭代器，通过 vield 关键字来创建,生成器运行时每次遇到 vield时,函数会暂停并保存当前运行信息，下次执行 next() 时从暂停位置继续运行





**验证码**

​	对于线上环境

​		如果是图片验证码,我会优先考虑ocr去识别图片上的字符,其实识别率不高,还不到50%

​			 1、简单验证码识别：

​			Pil模块截图 ddddocr模块做图片识别

​			把整个登录页面截图 确定验证码图片坐标 抠图 用ddddocr的classification方法识别验证码写到input框

​			2、复杂验证码：

​			调用付费第三方api的AI识别 

​			showapirequest/ddddocr模块处理有横线的验证码

​		如果是短信验证码，我会到验证码的存储位置去读，比如数据库读取

​	对于测试环境

​		可以让开发直接关闭验证码或者设置万能验证码

​		也可以将部分账号添加到白名单来跳过验证





**Jenkins每天都跑吗？**	

​	用jenkins定时晚上下班后跑一跑 隔天早上看看测试报告有没有异常



**描述符(类) 元素定位重新封装**	

​	1、实现 get set delete任意一个方法的类  

​	2、在get里写find_element然后传入一个键值对就能实现元素定位

​	3、在set里写的sendkeys 然后元素赋值的时候就会触发 set里的sendkeys实现赋值



**怎么选择执行测试用例**	

​	1、标记@pytest.mark. x然后用pytest -m x参数指定要运行的函数 2、指定包含表达式的函数pytest -k “” 3、指定目录 pytest test/



**全局管理driver**	

​	在conftest配置一个dirver函数 使用fixture的session参数 然后哪里需要用到driver的时候直接参入dirver就可以了



**有哪些断言**	

​	文本匹配断言 元素状态断言 元素存在断言 页面跳转断言 、难的场景：文件上传图片 图片是不是我所上传的 图片颜色识别



**元素定位xpath和css**	

​	Xpath功能强大 性能稍差



***selenium\*****中有哪些元素定位方式*****?\*****你如何决定使用哪种定位方式*****?\***

​	属性动态变化的元素怎么定位

​		先找出变化规律，在元素定位时，用规律去生成对应的要定位的属性即可

​	高亮的元素怎么定位

​		元素高亮一般css样式设置的,可以根据css选择器进行定位隐藏的元素怎么定位

​	隐藏元素的定位方式和可见元素是一样的，只不过可能无法对其进行交互操作

​		可以使用js脚本来绕过这些限制

​	定位不到元素会有哪些情况

​		可能是动态元素,属性不固定

​		可能元素被遮挡,需要最太化窗口或滚动页面才可见 

​		可能元素在iframe中,需要切换iframe

​	页面元素没办法提取怎么办

​		可以用pyautoGUl做图像识别

有id, name, class_name, tag_ name, link text, partial link text, xpath,css selector等八种定位方式

我一般会先考虑id定位,

如果元素没有id,再考虑xpath或css selector,因为浏览器可以直接导出表达式



**显示等待和隐式等待是什么意思，和sleep函数有什么区别?**

​	元素等待是为了确保页面元素加载完成的手段隐式等待是设置一个全局的等待时间,如果定位元素超时会报NoSuchElementException异常0显式等待可以为定位不同元素设置不同的超时时间,更加灵活,定位超时会报TimeoutException异常0time.sleep(3)是强制等待,直接暂停线程,用法比较暴力



**你们UI自动化的用例数,覆盖率，通过率数据是多少?**

​	上个项目我跟了一年,总用例数大概3000条左右,其中大概有1000条左右是需要自动化回归的测试用例我们做UI自动化的覆盖率目标是30%,基本都完成了

还有一部分接口没有覆盖的原因是:某些功能的使用率较低,部分功能涉及支付和第三方服务,还有一些涉及0硬件操作的用例,比如扫码入库,这些我都是手工完成回归的通过率基本都是100%,毕竟都是旧功能了











## Python

我用python写了个工具，可以生成对应格式和大小的文件 	我们公司文件上传的功能较多,我就写了一个工具,

​	可以生成对应格式和大小的文件

可变数据类型：列表list 集合set 字典dict ；改变对象内部的值 内存地址不变

不可变数据类型：int float 布尔 字符串str 元组tuple ；创建后对象里的值不能改变，修改是创建新的对象 内存地址会变 

列表[]存储动态变化的数据 可以增删改查

元组()储存不变的数据 只能查询，元组是只读的列表 元组的性能优于列表

列表去重：

使用集合的特性

先用set函数把列表转换为集合 再用list函数把类型转换回列表

循环遍历方法去重

先定义一个空列表 然后循环遍历原列表元素 如果元素不在空列表 用append方法把元素添加进去



字符串反转：

切片的方式 设置步长为-1即可

内置函数的方法思路是先使用reversed函数反转，再使用join函数进行拼接

浅拷贝 深拷贝：

本质，在于 Python 的变量赋值默认是引用传递。浅拷贝只复制第一层结构的引用，而深拷贝会递归复制所有层级的数据对象，从而避免多个变量共享同一数据时产生的联动问题变量赋值让多个变量引用同一块数据

都用copy模块实现 浅拷贝copy函数 深拷贝deepcopy函数

对于不可变类型的数据 浅拷贝和深拷贝都 没有新建外内层对象 就复制数据的引用 不会开辟新的内存地址

对于可变类型的数据

浅拷贝 只新建外层对象 外层开辟新的内存地址 复制数据的值，内层的数据只复制引用 内层对象共享

深拷贝 新建外内层对象 内外层都开辟新的内存地址 把值复制过来

冒泡：

核心是两层嵌套循环来实现

外层控制循环的轮次，每一轮找出当前最符合的元素，并冒泡

内层控制每个元素两两比较的次数，以及元素位置的交换



**说下python中的推导式?**

​	用于从一个可迭代对象中创建新的容器

​	比如 [x**2 for x in range(1,11)]用于创建一个包含1到10的平方的列表



python中如何跳出循环?

​	break,用于结束循环

​	continue,用于跳出本次循环,直接进入下一次循环



列表中的数据如何拼接成字符串?

​	可以先定义空串，在通过for循环和+运算符来拼接列表中的数据

​	可以用字符串的join()方法,列表作为参数传进去就得到拼接后的字符串了



如何通过切片获取一个数据中倒数的3个元素?

​	首先很多数据类型都支持切片的操作,比如字符串,列表,元组等

​	切片的语法是储存数据的变量名后面跟个中括号,中括号内分别是起始位,结束位 和 步长

​	那么想获取倒数的三个元素只需要设置起始位为负3即可(形式如:变量名[-3:]



字典怎么遍历?

​	变量名.keys() 获取键列表

​	变量名.values() 获取值列表

​	变量名.items()获取包含了键和值的元组的列表



如何合并两个列表或字典?

​	合并列表可以用+运算符或list1.extend(list2)的方法

​	合并两个字典使用{**dict1，**dict2}或dict1.update(dict2)方法



如何捕获一个异常?

​	可以使用 try….except . 语法来捕捉异常,

​	如果后续有需要执行的代码可以放在 finally 代码块中



python函数传参时的*和**是什么意思?

​	*用于接收不确定个数的参数,并打包成一个元组,定义形参时通常用*args *用于处理元组/列表等数据

​	**用于处理字典数据









## Docker

```dockerfile
# mysql
docker volume create mysql_data

docker run --name car-mysql \
    -v mysql_data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=123456 \
    -e MYSQL_DATABASE=car \
    -e MYSQL_USER=test \
    -e MYSQL_PASSWORD=test-pass \
    -p 3306:3306 \
    -d mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

```dockerfile
# redis.conf
port 6379
bind 0.0.0.0
protected-mode no
dir /data
dbfilename dump.rdb
save 900 1
save 300 10
save 60 10000
appendonly no

docker volume create redis-data

docker run --name car_redis \
	-v $(pwd)/redis.conf:/etc/redis/redis.conf \
	-v redis-data:/data \
	-p 6379:6379 \
	-d redis redis-server /etc/redis/redis.conf
```

```dockerfile
# rabbitmq
docker volume create rabbitmq-data

docker run -d \
    --name rabbitmq \
    -p 5672:5672 \
    -p 15672:15672 \
    -v rabbitmq_data:/var/lib/rabbitmq \
    -e RABBITMQ_DEFAULT_USER=admin \
    -e RABBITMQ_DEFAULT_PASS=123456 \
    rabbitmq:management
```

```dockerfile
# vue-nginx
docker build -t nginx-vue .

docker save -o nginx-vue.tar nginx-vue

sudo docker load -i /root/nginx-vue.tar 
docker run -d -p 80:80 --privileged=true nginx-vue
```

```dockerfile
# _back
docker build -t car_back .

docker save -o car_back.tar car_back

sudo docker load -i /root/car_back.tar
docker run -d --name car_back -p 8000:8000 car_back
```

```
# 进入容器
docker exec -it ID bash
```

```
# volume
docker volume ls

docker volume inspect rabbitmq-data
```

```
# 权限问题
docker exec -it competent_mendeleev chmod 644 /usr/share/nginx/html/index.html

docker exec -it competent_mendeleev find /usr/share/nginx/html/ -type f ! -perm -o=r -ls

docker exec -it competent_mendeleev find /usr/share/nginx/html/ -type f ! -perm -o=r -exec chmod 644 {} \;
docker exec -it competent_mendeleev find /usr/share/nginx/html/ -type f ! -perm -o=r -ls
```

```
# 手动加载插件
# 进入mysql
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
FLUSH PRIVILEGES;
```



## Jenkins

下载钉钉插件 系统管理里新增机器人 任务里添加机器人

<img src="/Users/chu/Library/Application Support/typora-user-images/image-20250526212540794.png" alt="image-20250526212540794" style="zoom:30%;" />

<img src="/Users/chu/Library/Application Support/typora-user-images/image-20250526212738553.png" alt="image-20250526212738553" style="zoom:25%;" />

下载GitHub git插件，系统管理添加凭据，系统配置里添加GitHub服务器、配置git、配置定时构建、执行shell

全局工具配置git 配置allure



实现自动化代码CI流程：

​	代码传到GitHub仓库 GitHub仓库设置webhook 在Jenkins上配置GitHub服务器

​	在jenkins的任务里写shell脚本，配置钉钉机器人

​	生成allure报告 触发器选择github hook

​	实现webhook触发 GitHub仓库更新代码Jenkins就自动构建 和 定时构建 并且生成allure报告 通知钉钉

​		其中jenkins监听触发条件然后执行任务

​		定时构建就是Jenkins主动从GitHub拉取 在Jenkins配置git地址 任务里源码管理填写GitHub仓库地址和账户密码 设置定时构建

​		webhook触发 先在GitHub项目里配置webhook 填写Jenkins地址和secret 然后把secret添加到jenkins凭据 配置GitHub服务器信息 任务里面配置secret 构建触发器选择 GitHub hook 步骤里写个shell执行pytest命令

   			*GitHub*发送*webhook*请求的时候通过*paylod*和*secret*使用*HMAC-SHA256*计算签名
   	
   			*jenkins*自动使用*GitHub*发送来的*payload*和本地存储的*secret*用同样的方法*HMAC-SHA256*计算签名
   	
   			*jenkins*自动把两个签名进行对比

 下载allure插件 配置allure的地址 任务里构建后操作 配置json的文件路径

 下载钉钉插件 钉钉群添加自定义机器人secret 然后在Jenkins配置钉钉 填写webhook地址和secret 并在任务里添加



DevOps是一种把开发和运维紧密结合文化 

GitOps是DevOps文化的实现方式 由iac+git+cicd流水线组成 

​	iac是用代码管理 自动化配置

​	cicd流水线分为pull push模式

​		push模式是Jenkins主动拉取GitHub的代码 构建打包 把生成的产物推送到服务器 运行实例 实现项目部署上线

​		pull模式是把代码打包生成docker镜像 上传到镜像仓库 服务器(tomato)主动从镜像仓库 pull把镜像拉过来 运行前后端docker实例 通过k8s部署上线 中间argo cd监控他们的状态 实现项目部署上线

​			argo cd就是去管理k8s集群 可以去创建项目 ，这个项目只要他的状态和git仓库状态不一致的时候说明git仓库有代码变化 会主动去同步一下中间间实现cd全过程 自动构建自动部署 最终可以用url访问改动过的网站













Jenkins拉取前后端代码 —— docker部署（前端：nginx.conf配置地址转发，创建dockerfile把打包好的dist放到nginx里 暴露端口 运行）



git push - Jenkins构建 - docker镜像打包 - 推送仓库 - 部署运行

CI持续集成 自动化

CD通过docker项目前后端代码部署上线



docker的使用：

docker容器技术 把应用打包成镜像(前后端) 运行成容器(测试环境 上线) ；容器和容器之间相互隔离 互相通信

运维写好环境部署脚本 然后我使用jenkins的一键部署功能

​	制作本地镜像仓库

​	使用docker build基于dockerfile分别制作 前后端镜像 并通过docker push上传到本地仓库备份

​	通过docker run运行前后端镜像,生成对应的实例

​	然后就可以访问了

​	（合理分配 最大化利用服务器资源；环境部署能做到各个测试/预生产环境一致；一致性 隔离性 易于管理）

我工作中没有用到 docker，已经有一套完整的 cd 流水线了，不过我看过相关的学习资料和公司的搭建文档，我知道怎么用的



Jenkins的使用：

实现CI CD,租阿里云的服务器,运行Jenkins服务

CI持续集成

检测前后端git仓库代码变动 代码更新则触发自动部署测试环境

再通过git拉取最新的自动化测试代码,执行并生成alure测试报告,生成的测试报告发送到钉钉群

只有在dev分支上经过了自动化测试的代码 才会被提交到test以便进一步完成系统测试

CD持续部署

在验收测试通过之后,Jenkins会通过git把代码合并到主干

然后拉取主干最新代码进行构建,把代码转化为可执行docker镜像

然后执行运维配置好的部署脚本

​	docker镜像,通过push上传镜像到镜像仓库,再把镜像运行为实例，同时用到了k8s进行集群部署

jenkins也会用于线上巡检,定时每天凌晨3点运行一次自动化测试



​	docker compose：**声明式配置文件**描述整个应用 -使用一条命令完成部署

​	部署compose应用 默认读取docker-compose.yml/.yaml



最关键的有哪些指令:

docker pull :拉取镜像到本地

docker images :列出所有的镜像

docker ps :列出当前系统中正在运行的容器

docker commit :生成镜像

docker build :基于 dockerfile 生成镜像

docker exec-it jenkins bash :进入容器内部

docker run -it :把镜像运行成为实例对象

docker rm -f:删除镜像 docker rmi

exit:退出容器内部环境

docker logs+容器名称:查某个容器的 docker 日志



利用 docker 从0到1发布上线的整个过程：

1、我们要制作本地镜像仓库

2、利用 docker build 的方式基于 docker file 去制作含有网站代码以及各种依赖的前后端 docker 镜像，并利用 docker push 上传到本地仓库中【备份)

3、再利用 docker run 运行前后端镜像，并生成前后端实例

就说明部署成功

4、用户通过网址访问网站，并且接口也有正常响应数据的情况，



怎么在这个容器内去执行一些命令：

进入容器内部，这进去之后就可以执行其他命令了docker exec - it jenkins bash可以换成其他的。这里的jenkins 是容器的名称 可以换成别的



docker 怎么去拉一个镜像，怎么把它部署起来：

先 docker pull 镜像，然后再运行 docker run 镜像，最后生成 docker 的实例，就能部署起来了



怎么去 docker 里面去终止掉某个进程：

(先进去，再 kill)

docker exec -it jenkins /bin/bash

kill pid







-- docker里面运行mysql

docker run -d --name mysql_container \

 -e MYSQL_ROOT_PASSWORD=123456 \

 -e MYSQL_DATABASE=testdb \

 -p 3306:3306 \

 -v ~/docker/mysql/data:/var/lib/mysql \

 mysql:latest



-- docker里面运行Linux

docker run -d -it --name mywebserver -p 8080:80 ubuntu:latest

-- 进入Linux

docker exec -it linux_car bash



你在使用 docker 的过程中，常用的哪些命令：

Systemctl restart docker

docker stop 容器ID:停止运行的容器

docker push

docker built

docker run -it :重建，会丢容器内部的配置数据

docker start+lD 这一条命名和上一条命令有区别，不会丢失容器内部的配置数据容器 

docker restart +容器ID :重启容器

docker images

docker tag

docker cp 本地文件想上传到容器里面，怎么上传?说出命令?

Docker pull redis: ...tag

docker ps -a:列出当前系统中所有的容器(包括运行的或是已停止的)-all

docker ps :列出系统中正在运行的容器,不包括已经关闭的容器

Docker commit docker build 构建新镜像

Dockerfile:不是一个指令，是一个基于 docker build 的打包必须文件。Exit 退出

docker exec -it jenkins /bin/bash进入到正在运行的 docker 中，首先用 docker ps 看看名字

docker cp /root/gitUl_auto/automation/ df8b61fd9fcb:/var/ienkins home/workspace

这一串代码是将容器外部的代码放到 jenkins 内部的工作目录下



最关键的有哪些指令:

docker pull :拉取镜像到本地

docker images :列出所有的镜像

docker ps :列出当前系统中正在运行的容器

docker commit :生成镜像

docker build :基于 dockerfile 生成镜像

docker exec-it jenkins bash :进入容器内部

docker run -it :把镜像运行成为实例对象

docker rm -f:删除镜像 docker rmi

exit:退出容器内部环境

docker logs+容器名称:查某个容器的 docker 日志



利用 docker 从0到1发布上线的整个过程：

1、我们要制作本地镜像仓库

2、利用 docker build 的方式基于 docker file 去制作含有网站代码以及各种依赖的前后端 docker 镜像，并利用 docker push 上传到本地仓库中【备份)

3、再利用 docker run 运行前后端镜像，并生成前后端实例

就说明部署成功

4、用户通过网址访问网站，并且接口也有正常响应数据的情况，



你在工作中你怎么用 docker 的：

我工作中没有用到 docker，已经有一套完整的 cd 流水线了，不过我看过相关的学习资料和公司的搭建文档，我知道怎么用的



怎么在这个容器内去执行一些命令：

进入容器内部，这进去之后就可以执行其他命令了docker exec - it jenkins bash可以换成其他的。这里的jenkins 是容器的名称 可以换成别的



docker 怎么去拉一个镜像，怎么把它部署起来：

先 docker pull 镜像，然后再运行 docker run 镜像，最后生成 docker 的实例，就能部署起来了



怎么去 docker 里面去终止掉某个进程：

(先进去，再 kill)

docker exec -it jenkins /bin/bash

kill pid



**你是怎么使用Jenkins的**

​	公司租了一个阿里云的服务器,专门运行jenkins服务Jenkins服务搭建 

​	-**我用的mac 我在终端用 SSH 连接服务 安装 Jenkins 并配置**	**用 scp 命令传输文件**

​	Jenkins服务是我独立搭建的

​	[可选]我们公司主要使用lenkins完成了测试环境的一键部署脚本,脚本的实现过程是首先kil测试环境的后。端进程,移除war包,然后git拉取最新代码进行build,并远程拷贝新的war包到测试环境对应的tomcat中,最后启动tomcat

​	[可选]我们公司的lenkins主要用于CI持续集成

首先是高频检测前后端git仓库的代码变动,如发现代码更新,则触发自动部署测试环境然后再通过git拉去最新的自动化测试代码,执行并生成allure测试报告,生成的测试报告会通过邮件发送给相关人员

​	[可选]在dev分支上经过了自动化测试的代码会被提交到test以便进一步完成系统测试o[可选1我们公司的lenkins还会用于CD持续部署

在验收测试通过之后，Jenkins会通过git把代码合并到主干

然后拉去主干最新代码进行构建,把代码转化为可执行的iar包或war包(或docker镜像)然后执行运维配置好的部署脚本(如果是docker镜像,需通过push上传镜像到镜像仓库,再把镜像运行为实例,同时用到了k8s进行集群部署)

​	[可选]我们公司的jenkins也会用于线上巡检,定时每天凌晨3点运行一次自动化测试



**持续集成CI：在源代码变更后自动检测、拉取、构建的过程。**

**持续交付CD：则是自动化部署和发布的过程，确保代码可以随时可靠地发布到生产环境。**



**了解哪些Jenkins插件：**

​	gitee插件,提供与gitee的集成

​	allure插件,提供在线读取allure测试报告的功能

​	dingtalk插件,提供发送钉钉消息的功能

​	emailextension插件,允许配置和发送通知邮件

​	ssh插件,允许ssh远程连接

​	maven插件,提供对maven项目的支持

​	docker插件,提供与docker的集成,允许操作docker仓库和容器



**怎么在Jenkins查看测试报告：**

​	首先要在jenkins服务器上下载allure,并配置环境变量

​	然后在jenkins中下载allure插件

​	然后通过 构建后操作 就可以执行自动化测试和生成allure报告了

​	可以通过生成在线报告以及在线地址来访问,也可以通过邮件发送离线报告,打开离线报告进行访问



**配置Jenkins过程遇到的错误：**

​	遇到的什么错误这个倒是没有，你可以说是公司有专门的运维来维护Jenkins

​	测试这边一般只是使用Jenkins 



**如何配置Jenkins项目：**

​	首先新建任务,输入项目名称,选择"自由风格项目”

​	然后配置源码管理,构建触发器,构建步骤以及构建后操作即可



**钉钉集成：**

​	首先安装钉钉的插件

​	然后在钉钉群里面创建一个webhook的机器人安装好之后再系统管理里面找到钉钉配置webhook地址和加密在项目里面选择通知谁，什么时候通知，以及自定义消息的内容