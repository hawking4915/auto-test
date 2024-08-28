
#测试所需浏览器类型'chrome8.0'/'谷歌8.0'  'firefox'/'火狐'   'IE'/'ie'
browser = 'chrome'
browserPath = r'C:\TianShu_fat\driver'

#日志输出路径
outLogPath = r'C:/TianShu_fat/outlog/'

#项目名称
project_name = 'TianShu_fat'

# 项目登录URL
IP = ''
GUI_project_url ='http://tianshu.hl.fat/'
API_project_url ='http://auth.hl.fat/auth/form'
API_header = "http://tianshu.hl.fat"

#GUI登录页面元素定位（公用）
usernameId = "username" #用户名
passwordId = "password"  #密码
loginEle = '//button[text()="登录"]'  #登录

#进入系统成功,系统title中是包含以下文字
projectTitle = "星座综合管理平台"

#天枢星座综合管理平台用户登录用户名、密码,获取用户基本信息url
username = 'wangsn'
password = '123456789'

#oAuth2协议授权码登录
Client_id = '69b2ee9c0542491bb0eae5866ebfd66b'
Client_secret = 'b00e36e4949a4a739616bb9d46d518ad'
Redirect_uri = 'http://tianshu.hl.fat/#/oAuth/callBack'
Scope = 'san_yuan_api'
State = 'c0542491bb0e'
Response_type = 'code'
OAuth_authorize_url = 'http://auth.hl.fat/oauth/authorize'
OAuth_token_url = 'http://auth.hl.fat/oauth/token'

#测试报告存放路径:（前提）在report文件夹下建立一个子文件夹，以项目名称命名
report_path = './report'

#测试用例路径(可根据需要测试的用例修改其对应路径)
# test_path = './TestCase/Test_Demo'
# test_path = './TestCase/GUI_AutoTestCase'
# test_path = './TestCase/API_AutoTestCase'
test_path = './TestCase'
# test_path = './TestCase/API_AutoTestCase/API_00_GetSwaggerAPI'

#GUI测试结果截图路径(GUI测试用例只能联调，涉及源码截图路径）
img_path = 'img'
img_history_path = 'img_history'

#执行用例unittest.defaultTestLoader.discover——pattern参数数据
#'Test*.py':执行所有用例；'Test_API*.py'：执行接口测试用例；'Test_GUI*.py'：执行功能测试用例
# testCase ='Test_GUI_TS_Login_001_OAuth.py'
# testCase ='Test_API_TS_DataProtocol_003_Creat.py'
# testCase ='Test_API_TS*.py'
# testCase ='Test_GUI_TS*.py'
testCase = 'Test*.py'

#SwaggerAPI测试数据路径
SwaggerAPI_testdata_path = './TestData/SwaggerAPI_TestData.xlsx'  #SwaggerAPI联调路径????/
# SwaggerAPI_testdata_path = '../TestData/SwaggerAPI_TestData.xlsx'  #SwaggerAPI单调路径

#SwaggerAPI测试数据路径（爬取的原始数据）______未使用
SwaggerAPI_data_path = './TestData/SwaggerAPI_Data.xlsx'  #SwaggerAPI联调路径
# SwaggerAPI_data_path = '../TestData/SwaggerAPI_Data.xlsx'  #SwaggerAPI单调路径

#所有API测试数据路径
API_testdata_path = './TestData/API_TestData.xlsx'  #联调路径
# API_testdata_path = '../../../TestData/API_TestData.xlsx'  #单调路径


#爬取SwaggerAPI信息文档
SwaggerAPI_path = "./TestData/SwaggerAPI.xlsx" #联调路径
# SwaggerAPI_path = "../TestData/SwaggerAPI.xlsx"#单调路径

#API测试数据Excel表格sheet名称
API_Sheet1 = "接口管理"
API_Sheet2 = "菜单管理"
API_Sheet3 = "资源管理"
API_Sheet4 = "功能管理"
API_Sheet5 = "角色管理"
API_Sheet6 = "导航"
API_Sheet7 = "主题配置"
API_Sheet8 = "用户管理"
API_Sheet9 = "用户登录"
API_Sheet10 = "数据协议管理"
API_Sheet11 = "数据类型管理"
API_Sheet12 = "遥测处理方法"
API_Sheet13 = "飞行器管理"
API_Sheet14 = "测控设备列表"

#GUI测试数据路径
GUI_testdata_path = './TestData/GUI_TestData.xlsx' #联调路径
# GUI_testdata_path = "../../../TestData/GUI_TestData.xlsx" #单调路径

#GUI测试数据Excel表格sheet名称
GUI_Sheet1 = "接口管理"
GUI_Sheet2 = "菜单管理"
GUI_Sheet3 = "资源管理"
GUI_Sheet4 = "功能管理"
GUI_Sheet5 = "角色管理"
GUI_Sheet6 = "导航"
GUI_Sheet7 = "主题配置"
GUI_Sheet8 = "用户管理"
GUI_Sheet9 = "用户登录"
GUI_Sheet10 = "数据协议管理"
GUI_Sheet11 = "数据类型管理"
GUI_Sheet12 = "遥测处理方法"
GUI_Sheet13 = "飞行器管理"
GUI_Sheet14 = "测控设备列表"

GUI_Sheet15 = "Demo"

#图片测试数据：上传图片路径&信息
appId = '75fc84f005764f1f801a368befb3ddc1'
appToken = 'd174a1798ddc4762a56d5a0f6d6dea08'
picture_path = "./TestData/" #联调路径
# picture_path = "../../../TestData/" #单调路径


#接口响应数据写入文件夹responseData
txt_path = "./responseData/" #联调路径
# txt_path = "../../../responseData/" #单调路径

#接口详细信息写入文件夹TestData
excel_path = "./TestData/" #联调路径
# excel_path = "../TestData/" #单调路径

#邮件发送者邮箱（可自行配置）
sendmail = '2960443562@qq.com'
#QQ邮箱授权码（QQ邮箱设置中自行配置）
PassKey = 'xbyjaqmedanfdgeb'
#邮件接收者邮箱列表
receivemail = ['17691149210@163.com']
#邮件内容
body = """
    <h1>测试邮件</h1>
    <h2><font face="微软雅黑"> 你好：附件是<天枢星座管理平台>项目自动化测试报告，请查阅，谢谢！</font></h2>
    <h3><font style="color:red" face="微软雅黑">注意：请用Firefox或Chrome浏览器查阅附件</font></h3>
    """


