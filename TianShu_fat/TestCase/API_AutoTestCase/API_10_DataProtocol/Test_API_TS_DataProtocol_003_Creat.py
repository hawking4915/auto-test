# -----------------------------------------------------------
#     Test_NO.：Test_API_TS_DataProtocol_003_Creat
#     Test_Title：添加数据协议
#     Test_Precondition：
#     Test_Step：
#     Author：wangshinan
#     Date：
#     Remark:
# -----------------------------------------------------------

import unittest,sys
from method.out_log import logger
from method.excel_process import Get_excel_data,processing_attachData_Dict,processing_attachData_json,IfExistList
from method.txt_process import read_txt_Response_data
from config.ProjectInfo import API_Sheet10,API_testdata_path,username,password
from ddt import ddt,data,unpack
from method.Login import API_Login

class DataProtocol_Creat:

    def step(self,*args):
        SelectData = read_txt_Response_data('DataProtocol_SelectData.txt')
        msgList = []
        codeList = []
        for i in SelectData:
            msgList.append(i['msg'])
            codeList.append(i['code'])
        attach = processing_attachData_Dict(args[2])
        for i in attach:
            test_protocolType= IfExistList(msgList,codeList,i['protocolType'],'测试数据该类型')
            if test_protocolType is not None:
                i['protocolType'] = test_protocolType
        test_byteOrder = IfExistList(msgList,codeList, args[1]["byteOrder"],'测试数据该字节顺序')
        if test_byteOrder is not None:
            args[1]["byteOrder"] = test_byteOrder
        args[1]["formatList"] = attach
        testdata_json = processing_attachData_json(args[1])
        resp = args[3].post(url = args[0], data =testdata_json,headers={'Content-Type':'application/json'})
        print('<p>测试数据:%s</p>' % args[1])
        print('<p>访问地址:%s</p>' % resp.url)
        return resp

@ddt
class Test_API_TS_DataProtocol_003_Creat(unittest.TestCase):

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
    def test_API_TS_DataProtocol_003_Creat(self,testdata,url,firstURL,attach,hope,number,testNum):
        """
            添加数据协议
        """
        resp1 = DataProtocol_Creat().step(url,testdata,attach,self.session)
        self.Test_assert(number,testNum, hope, resp1.text,'in')

    def tearDown(self):
        logger.info("----------------------------------------------------------------")

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

if __name__ == '__main__':
    unittest.main()