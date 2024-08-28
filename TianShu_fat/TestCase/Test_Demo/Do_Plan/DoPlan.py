# -----------------------------------------------------------
#     Test_NO.：
#     Test_Title：做计划
#     Test_Precondition：
#     Test_Step：1、外部轨道接口-入库两行根数
#                2、轨道预报
#                3、做计划
#                4、发送计划
#     Author：wangshinan
#     Date：
#     Remark:
# -----------------------------------------------------------

from os.path import abspath
from method.files_process import moveFiles
from ddt import ddt,data,unpack
import unittest,sys,requests
from method.GUI_Action import GUI_Action,open_driver,quit
from method.excel_process import Get_excel_data
from method.out_log import logger
from method.Login import GUI_Login
from BeautifulReport import BeautifulReport
from config.ProjectInfo import GUI_testdata_path, GUI_Sheet13,browser,browserPath,img_path,img_history_path,username,password
from method.txt_process import write_txt_Response_data, delete_txt_BlankLine, clean_txt_Response_data


class DoPlan(GUI_Action):
    def step(self,*args):

    #爬取两行根数
        TwoLine = requests.get("http://www.celestrak.com/NORAD/elements/active.txt")
        write_txt_Response_data(TwoLine.text,'TwoLine.txt')
        delete_txt_BlankLine(TwoLine.text,'TwoLine.txt')

    #导入两行根数至某颗卫星


@ddt
class Test_DoPlan(unittest.TestCase):

    data_list = Get_excel_data(GUI_testdata_path,GUI_Sheet13, "GUI")

    def Test_assert(self, number, testNum, hope, result,assertMethod):
        errors = []
        print('<p>期望结果:%s</p>' % hope)
        print('<p>响应结果:%s</p>' % result)
        try:
            if assertMethod in ['in', 'IN', 'iN', 'In']:
                self.assertIn(hope, result, "Bug")
            else:
                self.assertEqual(hope, result, "Bug")
            logger.info('\033[1;46m测试结果 : Pass\033[0m')
            print('序号:%s，测试编号:%s，断言期望结果:%s，断言响应结果:%s ' % (number, testNum, hope, result))
        except Exception as e:
            errors.append('\033[1;46m测试结果 : Fail\033[0m')
            errors.append(str(e))
            errors.append('序号:%s，测试编号:%s，断言期望结果:%s，断言响应结果:%s ' % (number, testNum, hope, result))
        if len(errors):
            logger.error(errors[0])
            logger.error(errors[1])
            logger.error(errors[2])
            raise AssertionError(*errors)

    @classmethod
    def setUpClass(cls):
        cls.driver = open_driver(browser_type=browser, path=browserPath)
        GUI_Login(cls.driver).GUI_LoginWeb(username, password)
        clean_txt_Response_data("TwoLine.txt")

    def setUp(self):
        logger.info("Test case : %s" % self.__class__.__name__)

    @BeautifulReport.add_test_img()
    @data(*data_list[sys._getframe().f_code.co_name])
    @unpack
    def test_DoPlan(self,testdata,clickXpath,hopeXpath,attach,testNum,hope,number):
        """
            做计划：轨道——计划
        """
        driver = self.driver
        self.newDriver = DoPlan(driver)
        test_result =self.newDriver.step(testdata,clickXpath,hopeXpath,attach,driver)
        self.Test_assert(number,testNum, hope, str(test_result),'in')

    def tearDown(self):
        logger.info("----------------------------------------------------------------")

    @classmethod
    def tearDownClass(cls):
        quit(cls.driver)
        moveFiles(abspath(img_path), abspath(img_history_path), 'Test_DoPlan')


if __name__ == '__main__':
    unittest.main()