#coding=utf-8

# -----------------------------------------------------------
#     Test_NO.：
#     Test_Title：获取swagger所有服务API接口数据写入SwaggerAPI_TestData
#     Test_Precondition：
#     Test_Step：
#     Author：wangshinan
#     Date：2021/08/12 10:45:00
#     Remark:
# -----------------------------------------------------------

import unittest
import sys
from requests import get
from json import loads
from method.files_process import deleteFiles
from method.out_log import logger
from method.excel_process import Get_excel_data,write_excel
from config.ProjectInfo import SwaggerAPI_path,SwaggerAPI_data_path,API_header
from ddt import ddt,data,unpack

class Get_SwaggerAPI:

    def step(self,*args):
        logger.info("获取 Swagger——%s 接口信息" % args[1])
        resp =get(url=args[0])
        if resp.status_code == 200:
            respDict = loads(resp.text)
            Module_name = respDict["info"]["title"]  # 模块名称   sheet页
            All_APIlist = []
            number = 1
            for info in respDict["paths"].keys():
                for requestType in respDict["paths"][info].keys():
                    APIlist = []
                    requestDatalist = []
                    APIlist.append(number)  # 序号
                    testNum = "Test_API_TS_%s_%03d" % (args[1], number)
                    APIlist.append(testNum)  # 测试编号
                    APIlist.append(API_header + info)  # 接口地址
                    APIlist.append(" ")  # FirstURL
                    if "parameters" in respDict["paths"][info][requestType].keys():  # 请求参数
                        for requestData in respDict["paths"][info][requestType]["parameters"]:
                            requestDatalist.append(requestData["name"])
                        APIlist.append(":".join(requestDatalist))
                    else:
                        APIlist.append(" ")
                    APIlist.append(' code: 200, message: "success"')  # 期望结果
                    APIlist.append(" ")  # 附加
                    APIlist.append(requestType)  # 请求方式
                    APIlist.append(respDict["paths"][info][requestType]["tags"][0])  # 功能菜单
                    APIlist.append(respDict["paths"][info][requestType]["summary"])  # 接口名称
                    All_APIlist.append(APIlist)
                    number += 1
            write_excel('SwaggerAPI_Data.xlsx', Module_name, All_APIlist)
            logger.info("获取成功：%s接口信息写入'SwaggerAPI_Data.xlsx'文件" % args[0]) 
        else:
            logger.info("\033[1;35m获取失败：%s接口响应结果为空\033[0m" % args[0])
        return resp


@ddt
class Test_Get_SwaggerAPI(unittest.TestCase):

    data_list = Get_excel_data(SwaggerAPI_path, "swaggerURL", "API")

    def Test_assert(self, number, testNum, hope, result,assertMethod):
        errors = []
        print('<p>期望结果:%s</p>' % hope)
        print('<p>响应结果:%s</p>' % result)
        try:
            if assertMethod in ['in','IN','iN','In']:
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
        deleteFiles(SwaggerAPI_data_path)

    def setUp(self):
        logger.info("Test case : %s" % self.__class__.__name__)

    @data(*data_list[sys._getframe().f_code.co_name])
    @unpack
    def test_get_SwaggerAPI(self,testdata,swagger_API_URL,swagger_URL,Module,hope,number,testNum):
        """
            获取Swagger接口信息
        """
        resp1 = Get_SwaggerAPI().step(swagger_API_URL, Module)
        self.Test_assert(number, testNum, hope, resp1.text,'in')

    def tearDown(self):
        logger.info("----------------------------------------------------------------")

if __name__ == '__main__':
    unittest.main()






