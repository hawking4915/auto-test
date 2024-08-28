# -----------------------------------------------------------
#     Test_NO.：Test_API_TS_DataProtocol_009_Delete
#     Test_Title：删除数据协议
#     Test_Precondition：
#     Test_Step：
#     Author：wangshinan
#     Date：
#     Remark:
# -----------------------------------------------------------

import unittest,sys
from method.out_log import logger
from method.excel_process import Get_excel_data,IfExistList
from method.txt_process import read_txt_Response_data
from config.ProjectInfo import API_Sheet10,API_testdata_path,username,password
from ddt import ddt,data,unpack
from method.Login import API_Login
from TestCase.API_AutoTestCase.API_10_DataProtocol.Test_API_TS_DataProtocol_004_AllBaseInfo import DataProtocol_AllBaseInfo
from TestCase.API_AutoTestCase.API_10_DataProtocol.Test_API_TS_DataProtocol_006_OneDetailedInfo import DataProtocol_OneDetailedInfo

class DataProtocol_Delete:

    def step(self,*args):
        AllBaseInfo = read_txt_Response_data('DataProtocol_AllBaseInfo.txt')
        protoNameList = []
        protocolIdList = []
        for i in AllBaseInfo:
            protoNameList.append(i['protoName'])
            protocolIdList.append(i['protocolId'])
        # DataProtocol_AllBaseInfo.txt协议名称均为大写，该处根据协议名称找协议ID，协议名称大小写不是测试点,故小写均转换为大写
        args[1]['protocolId'] = args[1]['protocolId'].upper()
        test_protocolId = IfExistList(protoNameList,protocolIdList, args[1]['protocolId'], '测试数据该数据协议')
        if test_protocolId is not None:
            args[1]['protocolId']=test_protocolId
        new_Url = args[0] + args[1]['protocolId']
        resp = args[3].delete(url=new_Url)
        print('<p>测试数据:%s</p>' % args[1])
        print('<p>访问地址:%s</p>' % resp.url)
        return resp

@ddt
class Test_API_TS_DataProtocol_009_Delete(unittest.TestCase):

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
    def test_API_TS_DataProtocol_009_Delete(self,testdata,url,firstURL,attach,hope,number,testNum):
        """
            删除数据协议
        """
        resp1= DataProtocol_Delete().step(url,testdata,attach,self.session)
        self.Test_assert(number,testNum, hope, resp1.text,'in')

    def tearDown(self):
        logger.info("----------------------------------------------------------------")

    @classmethod
    def tearDownClass(cls):
        DataProtocol_AllBaseInfo().step('http://tianshu.hl.fat/agreement-mgr/v1.0/dataProtocol/selectAll', '', '', cls.session)
        DataProtocol_OneDetailedInfo().step('http://tianshu.hl.fat/agreement-mgr/v1.0/dataProtocol/', {'protocolId': '全部数据协议'}, '', cls.session)
        cls.session.close()

if __name__ == '__main__':
    unittest.main()