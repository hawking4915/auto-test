#coding=utf-8

import unittest
from BeautifulReport import BeautifulReport
from config.ProjectInfo import test_path,testCase,projectTitle,report_path
from method.out_log import logger
from method.send_mail import send_mail
from tomorrow import threads

# -----------------------------------------------------------
#     Title：执行测试用例V1.0-单个用例执行
#     Remark：优点：测试报告数据准确，outlog打印不会遗漏、错乱
#             缺点：自动化执行时间长
#     Result：
# -----------------------------------------------------------
def add_case(test_path=test_path,testCase=testCase):
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.discover(test_path, pattern=testCase))
    return suite

def run_case(test_suite):
    logger.info("Project：%s" % projectTitle)
    logger.info("*************************  Test Start  *************************")
    if 'API' in testCase:
        report_filename = 'API_Test_report'
        report_description = 'API测试用例执行情况'
    elif 'GUI' in testCase:
        report_filename = 'GUI_Test_report'
        report_description = 'GUI测试用例执行情况'
    else:
        report_filename = 'Test_report'
        report_description = '测试用例执行情况'
    result =BeautifulReport(test_suite)
    report_path_ok = result.report(log_path = report_path, filename= report_filename, description=report_description)
    return report_path_ok

if __name__ == '__main__':
    suite = add_case()
    report_path_ok =  run_case(suite)
    print("\n")
    print('%s:2 >> 点击查询测试报告.' % report_path_ok)
    # send_mail(report_path_ok,ProjectInfo.body)



# -----------------------------------------------------------
#     Title：执行测试用例V2.0-多线程执行用例
#     Remark：优点：减少自动化执行时间
#             缺点：1.当多线程同时运行多个.py文件的用例时，测试报告中，报告汇总、饼状图区域、测试结果内容数据不准确。
#                  2.pycharm控制台打印outlog会遗漏一些输出，会影响问题的定位
#     Result：不采用
# -----------------------------------------------------------
# def add_case(test_path=ProjectInfo.test_path,testCase=ProjectInfo.testCase):
#     discover = unittest.defaultTestLoader.discover(test_path, pattern=testCase)
#     return discover
#
# @threads(3)
# def run_case(all_case):
#     if 'API' in ProjectInfo.testCase:
#         report_filename = 'API_Test_report'
#         report_description = 'API测试用例执行情况'
#     elif 'GUI' in ProjectInfo.testCase:
#         report_filename = 'GUI_Test_report'
#         report_description = 'GUI测试用例执行情况'
#     else:
#         report_filename = 'Test_report'
#         report_description = '测试用例执行情况'
#     print (all_case)
#     print("开始，现在时间是%s"%time.strftime("%Y-%m-%d %H_%M_%S"))
#     # '''执行所有的用例，并把结果写入测试报告'''
#     result =BeautifulReport(all_case)
#     result.report(log_path = ProjectInfo.report_path, filename= report_filename, description=report_description)
#
# if __name__ == "__main__":
#     cases = add_case()
#     for i in cases:
#        run_case(i)



