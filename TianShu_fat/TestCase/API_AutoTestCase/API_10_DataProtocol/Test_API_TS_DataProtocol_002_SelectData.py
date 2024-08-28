# -----------------------------------------------------------
#     Test_NO.：Test_API_TS_DataProtocol_002_SelectData
#     Test_Title：数据协议页面下拉框数据
#     Test_Precondition：
#     Test_Step：
#     Author：wangshinan
#     Date：
#     Remark:
# -----------------------------------------------------------

import unittest,sys
from json import loads
from method.out_log import logger
from method.excel_process import Get_excel_data
from config.ProjectInfo import API_Sheet10,API_testdata_path,username,password
from ddt import ddt,data,unpack
from method.Login import API_Login
from method.txt_process import write_txt_Response_data,clean_txt_Response_data


class DataProtocol_SelectData:

    def step(self,*args):
        resp = args[3].get(url = args[0])
        if '"code":200' and '"message":"success"' in resp.text:
            logger.info("请求数据协议页面下拉框数据-Success.")
            clean_txt_Response_data('DataProtocol_SelectData.txt')
            resp_Dict = loads(resp.text)
            for i in resp_Dict["data"]["byteOrderEnum"]:
                write_txt_Response_data(str(i), 'DataProtocol_SelectData.txt')
            for j in resp_Dict["data"]["protoTypeEnum"]:
                write_txt_Response_data(str(j), 'DataProtocol_SelectData.txt')
        else:
            logger.info("\033[1;35m请求数据协议页面下拉框数据-Fail.\033[0m")
        print('<p>测试数据:%s</p>' % args[1])
        print('<p>访问地址:%s</p>' % resp.url)
        return resp

@ddt
class Test_API_TS_DataProtocol_002_SelectData(unittest.TestCase):

    data_list = Get_excel_data(API_testdata_path, API_Sheet10, "API")

    def Test_assert(self, number, testNum, hope, result,assertMethod):
        errors = []
        print('<p>期望结果:%s</p>' % hope)
        print('<p>响应结果:%s</p>' % result)
        try:
            if assertMethod in ['in', 'IN', 'iN', 'In']:
                self.assertIn(hope, result, "Bug")
            else:
                self.assertEqual(hope, result, "Bug")
            logger.info('\033[1;42m测试结果 : Pass\033[0m')
            print('序号:%s，测试编号:%s，断言期望结果:%s，断言响应结果:%s ' % (number, testNum, hope, result))
        except Exception as e:
            errors.append('\033[1;41m测试结果 : Fail\033[0m')
            errors.append(str(e))
            errors.append('序号:%s，测试编号:%s，断言期望结果:%s，断言响应结果:%s ' % (number, testNum, hope, result))
        if len(errors):
            logger.error(errors[0])
            logger.error(errors[1])
            logger.error(errors[2])
            raise AssertionError(*errors)

    @classmethod
    def setUpClass(cls):
        cls.token,cls.session = API_Login().API_LoginWeb(username,password)

    def setUp(self):
        logger.info("Test case : %s" % self.__class__.__name__)

    @data(*data_list[sys._getframe().f_code.co_name])
    @unpack
    def test_API_TS_DataProtocol_002_SelectData(self,testdata,url,firstURL,attach,hope,number,testNum):
        """
            数据协议页面下拉框数据
        """
        resp1 = DataProtocol_SelectData().step(url,testdata,attach,self.session)
        self.Test_assert(number,testNum, hope, resp1.text,'in')

    def tearDown(self):
        logger.info("----------------------------------------------------------------")

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

if __name__ == '__main__':
    unittest.main()