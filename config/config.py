# 环境基准地址
# BASE_URL = "https://cloud.gyjerp.com"
BASE_URL = "http://60.204.225.104:9632"

# excel格式的测试用例文件配置。
EXCEL_FILE = "./data/测试用例完整版.xlsx"
SHEET_NAME = "Sheet1"

# mysql配置
DB_HOST = "60.204.225.104"
DB_PORT = 3306
DB_NAME = "mydb"
DB_USER = "api"
DB_PASSWORD = "xiaobeiup"

# mysql资源销毁
# SQL1 = 'DELETE from base_data_store_center where code = "bm_ck_04" or code = "bm_ck_05"'
SQL1 = 'select * from sp_user'
SQL2 = 'select * from sp_order'
# SQL2 = """DELETE from op_logs where extra = '{"code":"bm_ck_04","name":"北梦测试仓库4"}' or extra = '{"code":"bm_ck_05","name":"北梦测试仓库5"}'"""



