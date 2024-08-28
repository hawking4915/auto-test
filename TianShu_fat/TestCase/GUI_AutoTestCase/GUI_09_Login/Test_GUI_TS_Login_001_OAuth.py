# -----------------------------------------------------------
#     Test_NO.：Test_GUI_TS_Login_001_OAuth
#     Test_Title：用户登录
#     Test_Precondition：
#     Test_Step：
#     Author：wangshinan
#     Date：
#     Remark:
# -----------------------------------------------------------

import unittest,sys
from os.path import abspath
from config.ProjectInfo import GUI_project_url,GUI_testdata_path, GUI_Sheet9,browser,browserPath,img_path,img_history_path
from ddt import ddt,data,unpack
from method.GUI_Action import GUI_Action,open_driver,quit
from selenium.webdriver.common.by import By
from method.out_log import logger
from BeautifulReport import BeautifulReport
from method.excel_process import Get_excel_data
from method.files_process import moveFiles

class Login_OAuth(GUI_Action):

    def step(self,*args):
        self.open_url(GUI_project_url)
        self.page_loading()
        self.window_size("最大化")
        self.sendKeys_element(By.ID, args[1][0], args[0][0], args[3][0])
        self.sendKeys_element(By.ID, args[1][1], args[0][1], args[3][1])
        self.click_element( By.XPATH, args[1][2], args[3][2])
        BeautifulReport.save_img(args[4], "手动截图_点击登录之后")
        test_result = self.get_text( By.CSS_SELECTOR, args[2][0])
        return test_result


@ddt
class Test_GUI_TS_Login_001_OAuth(unittest.TestCase):

    data_list = Get_excel_data(GUI_testdata_path, GUI_Sheet9, "GUI")

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

    def setUp(self):
        self.driver = open_driver(browser_type=browser, path=browserPath)
        logger.info("Test case : %s" % self.__class__.__name__)

    @BeautifulReport.add_test_img("手动截图_点击登录之后")
    @data(*data_list[sys._getframe().f_code.co_name])
    @unpack
    def test_GUI_TS_Login_001_OAuth(self,testdata,clickXpath,hopeXpath,attach,hope,testNum,number):
        """
            用户登录
        """
        driver = self.driver
        self.newDriver = Login_OAuth(driver)
        test_result = self.newDriver.step(testdata, clickXpath, hopeXpath, attach,driver)
        self.Test_assert(number,testNum, hope[0], test_result,'in')

    def tearDown(self):
        quit(self.driver)
        logger.info("----------------------------------------------------------------")

    @classmethod
    def tearDownClass(cls):
        moveFiles(abspath(img_path), abspath(img_history_path),'Test_GUI_TS_Login_001_OAuth')


if __name__ == '__main__':
    unittest.main()