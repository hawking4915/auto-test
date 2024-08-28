# -----------------------------------------------------------
#     Test_NO.：
#     Test_Title：统计轨道预报的时间
#     Test_Precondition：
#     Test_Step：
#     Author：wangshinan
#     Date：
#     Remark:
# -----------------------------------------------------------


from method.Login import GUI_Login,API_Login
import unittest,sys,datetime,json
from ddt import ddt,data,unpack
from os.path import abspath
from method.files_process import moveFiles
from method.GUI_Action import GUI_Action,open_driver,quit
from method.out_log import logger
from method.excel_process import Get_excel_data
from method.txt_process import clean_txt_Response_data,write_txt_Response_data
from BeautifulReport import BeautifulReport
from config.ProjectInfo import GUI_testdata_path, GUI_Sheet13,browser,browserPath,img_path,img_history_path,username,password

class OrbitPrediction_Time(GUI_Action):

    def step(self,*args):
        #获取鸿雁首发星六根数数据
        token, session =API_Login().API_LoginWeb('wangsn', '123456')
        resp = session.get("http://orbitcalc.hl.fat/orbitcalc-mgr/v1.0/prediction/param/allParamInfo/1")
        w = json.loads(resp.text)

        #鸿雁首发星六根数数据写入文档
        write_txt_Response_data(str(w['data']), 'OrbitPrediction_0001.txt')
        session.close()

        #进入控制
        self.click_element(By.LINK_TEXT, args[1][0], args[3][0])
        BeautifulReport.save_img(args[4], "手动截图_点击控制")

        #进入轨道预报页面
        self.click_element(By.XPATH, args[1][1], args[3][1])
        BeautifulReport.save_img(args[4],"手动截图_点击轨道预报")
        result = self.is_text_in_element(args[3][10],By.XPATH, args[1][1])

        # #获取鸿雁首发星六根数数据
        # ID = w['data']['spacecraftId']
        # name = w['data']['spacecraftName']
        # code = w['data']['spacecraftCode']
        # selectName = name+" / "+code
        # startTime = w['data']['liyuanDateStr']
        # ST = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S.%f')
        # endTime = (ST + datetime.timedelta(hours = int(args[0][0]))).strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
        #
        # #赋值
        # self.sendKeys_element( By.CSS_SELECTOR, args[1][2],selectName,args[3][2])
        # self.sendKeys_element(By.CSS_SELECTOR, args[1][3],startTime,args[3][3])
        # self.sendKeys_element(By.CSS_SELECTOR, args[1][4],endTime, args[3][4])

        # #点击开始计算
        # self.click_element( By.CSS_SELECTOR, args[1][5], args[3][5])
        # StartPredictionTime =  datetime.datetime.now()
        #
        # #判断计算完成
        # while True:
        #     result2 = self.get_text( By.XPATH, args[1][6])
        #     logger.info(result2)
        #     if args[3][6] in result2:
        #         EndPredictionTime = datetime.datetime.now()
        #
        #         #预报完成所需时间
        #         PredictionTime_Sec = (EndPredictionTime - StartPredictionTime ).total_seconds()
        #         PredictionTime_Min= PredictionTime_Sec/60
        #
        #         #写入文件
        #         data = {"预报时间段":args[3][2],"startTime":startTime,"endTime":endTime,"PredictionTime_Min":PredictionTime_Min,"PredictionTime_Sec":PredictionTime_Sec}
        #         dataProcess.write_Response_data(str(data), "OrbitPredictionTime.txt")
        #         break
        #     else:
        #         continue
        #
        # #判断计算有结果
        # self.click_element(By.XPATH, args[1][6], args[3][7])
        # self.click_element(By.CSS_SELECTOR, args[1][7], args[3][8])
        # self.time_wait(2)
        # result = self.is_text_in_element(args[3][9],By.XPATH, args[2])
        # if result:
        #     print("预报计算结果_Success")
        # else:
        #     print("预报计算结果_Fail")
        return result

@ddt
class Test_OrbitPredictionTime(unittest.TestCase):

    data_list = Get_excel_data(GUI_testdata_path, GUI_Sheet13, "GUI")

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
        clean_txt_Response_data("OrbitPrediction_0001.txt")
        cls.driver = open_driver(browser_type=browser, path=browserPath)
        GUI_Login(cls.driver).GUI_LoginWeb(username, password)

    def setUp(self):
        logger.info("Test case : %s" % self.__class__.__name__)

    @BeautifulReport.add_test_img("手动截图_点击轨道预报","手动截图_点击控制")
    @data(*data_list[sys._getframe().f_code.co_name])
    @unpack
    def test_OrbitPredictionTime(self,testdata,clickXpath,hopeXpath,attach,testNum,hope,number):
        """
            轨道预报：统计轨道预报的时间
        """
        self.newDriver = OrbitPrediction_Time(self.driver)
        test_result =self.newDriver.step(testdata,clickXpath,hopeXpath,attach,self.driver)
        self.Test_assert(number,testNum, hope, str(test_result),'in')

    def tearDown(self):
        logger.info("----------------------------------------------------------------")

    @classmethod
    def tearDownClass(cls):
        quit(cls.driver)
        moveFiles(abspath(img_path), abspath(img_history_path), 'Test_ImportTLE')


if __name__ == '__main__':
    unittest.main()