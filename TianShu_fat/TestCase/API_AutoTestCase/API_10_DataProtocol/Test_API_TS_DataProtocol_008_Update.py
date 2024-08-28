# -----------------------------------------------------------
#     Test_NO.：Test_API_TS_DataProtocol_008_Update
#     Test_Title：修改数据协议
#     Test_Precondition：
#     Test_Step：
#     Author：wangshinan
#     Date：
#     Remark:
# -----------------------------------------------------------

import unittest,sys
from method.out_log import logger
from method.excel_process import Get_excel_data, processing_attachData_json,processing_attachData_Dict,IfExistList
from method.txt_process import read_txt_Response_data
from config.ProjectInfo import API_Sheet10,API_testdata_path,username,password
from ddt import ddt,data,unpack
from method.Login import API_Login
from TestCase.API_AutoTestCase.API_10_DataProtocol.Test_API_TS_DataProtocol_004_AllBaseInfo import DataProtocol_AllBaseInfo
from TestCase.API_AutoTestCase.API_10_DataProtocol.Test_API_TS_DataProtocol_006_OneDetailedInfo import DataProtocol_OneDetailedInfo

class DataProtocol_Update:

    def step(self,*args):
        SelectData = read_txt_Response_data('DataProtocol_SelectData.txt')
        msgList = []
        codeList = []
        for i in SelectData:
            msgList.append(i['msg'])
            codeList.append(i['code'])
        AllDetailedInfo = read_txt_Response_data('DataProtocol_OneDetailedInfo.txt')
        protoNameList = []
        for i in AllDetailedInfo:
            protoNameList.append(i['protoName'])
        protoInfo = IfExistList(protoNameList, AllDetailedInfo,args[1]['protocolId'], '测试数据该数据协议')
        if protoInfo is not None:
            args[1]['createdBy'] = protoInfo['createdBy']
            args[1]['createdTime'] = protoInfo['createdTime']
            args[1]['updatedBy'] = protoInfo['updatedBy']
            args[1]['updatedTime'] = protoInfo['updatedTime']
            args[1]['protocolId'] = protoInfo['protocolId']
            if args[1]['protoName'] ==  '数据协议名称':
                args[1]['protoName'] = protoInfo['protoName']
            else:
                logger.info("数据协议名称（%s）修改为（%s）." % (protoInfo['protoName'], args[1]['protoName']))
            if args[1]['byteOrder'] ==  '字节顺序':
                args[1]['byteOrder'] = protoInfo['byteOrder']
            else:
                test_byteOrder= IfExistList(msgList, codeList,args[1]['byteOrder'], '修改数据该字节顺序')
                if test_byteOrder is not None:
                    args[1]['byteOrder'] = test_byteOrder
                logger.info("字节顺序（%s）修改为（%s）." % (protoInfo['byteOrder'], args[1]['byteOrder']))
            attach = processing_attachData_Dict(args[2])[0]
            IndexList = []
            for i in protoInfo['formatList']:
                IndexList.append(i['index'])
            if  int(attach['index']) in IndexList:
                logger.info("修改数据协议名称（%s）的数据协议格式，序号为（%s）." % (protoInfo['protoName'], attach['index']))
                format = protoInfo['formatList'][int(attach['index'])-1]
                if  attach['formatName'] != '代号':
                    logger.info("代号（%s）修改为（%s）." % (format['formatName'], attach['formatName']))
                    format['formatName'] = attach['formatName']
                else:
                    pass
                if  attach['byteLoacl'] != '字节位':
                    logger.info("字节位（%s）修改为（%s）." % (format['byteLoacl'], attach['byteLoacl']))
                    format['byteLoacl'] = attach['byteLoacl']
                else:
                    pass
                if  attach['orderBit'] != '位序':
                    logger.info("位序（%s）修改为（%s）." % (format['orderBit'], attach['orderBit']))
                    format['orderBit'] = attach['orderBit']
                else:
                    pass
                if  attach['protocolType'] != '类型code':
                    test_protocolType = IfExistList(msgList,codeList, attach['protocolType'], '修改数据该类型')
                    if test_protocolType is not None:
                        format['protocolType'] = test_protocolType
                    protocolType = IfExistList(codeList, msgList,format['protocolType'], '修改数据该类型')
                    logger.info("类型（%s）修改为（%s）." % (protocolType, attach['protocolType']))
                else:
                    pass
                if  attach['mark'] != '备注':
                    logger.info("备注（%s）修改为（%s）." % (format['mark'], attach['mark']))
                    format['mark'] = attach['mark']
                else:
                    pass
                if  attach['protocolValue'] != '值':
                    logger.info("值（%s）修改为（%s）." % (format['protocolValue'], attach['protocolValue']))
                    format['protocolValue'] = attach['protocolValue']
                else:
                    pass
                args[1]['formatList'] = protoInfo['formatList']
            else:
                args[1]['formatList'] = protoInfo['formatList']
        testdata_json = processing_attachData_json(args[1])
        resp = args[3].put(url=args[0], data =testdata_json,headers={'Content-Type':'application/json'})
        print('<p>测试数据:%s</p>' % args[1])
        print('<p>访问地址:%s</p>' % resp.url)
        return resp

@ddt
class Test_API_TS_DataProtocol_008_Update(unittest.TestCase):

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
    def test_API_TS_DataProtocol_008_Update(self,testdata,url,firstURL,attach,hope,number,testNum):
        """
            修改数据协议
        """
        resp1= DataProtocol_Update().step(url,testdata,attach,self.session)
        self.Test_assert(number,testNum, hope, resp1.text,'in')

    def tearDown(self):
        logger.info("----------------------------------------------------------------")

    @classmethod
    def tearDownClass(cls):
        DataProtocol_AllBaseInfo().step('http://tianshu.hl.fat/agreement-mgr/v1.0/dataProtocol/selectAll', '', '',cls.session)
        DataProtocol_OneDetailedInfo().step('http://tianshu.hl.fat/agreement-mgr/v1.0/dataProtocol/',{'protocolId': '全部数据协议'}, '', cls.session)
        cls.session.close()

if __name__ == '__main__':
    unittest.main()