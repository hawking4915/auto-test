# -----------------------------------------------------------
#     Test_NO.：Test_API_TS_Login_001_OAuth
#     Test_Title：用户登录
#     Test_Precondition：
#     Test_Step：
#     Author：wangshinan
#     Date：
#     Remark:
# -----------------------------------------------------------

import unittest,sys,requests
from os import environ
from requests_oauthlib import OAuth2Session
from method.out_log import logger
from method.txt_process import write_txt_Response_data,clean_txt_Response_data
from method.excel_process import Get_excel_data
from config.ProjectInfo import Client_id,Client_secret,Redirect_uri,Scope,State,OAuth_authorize_url,API_project_url,\
    OAuth_token_url,API_Sheet9,API_testdata_path
from ddt import ddt,data,unpack

class user_OAuthLogin:

    def step(self,*args):
        environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'#This allows us to use a plain HTTP callback
        session = OAuth2Session(Client_id, redirect_uri=Redirect_uri,scope=Scope, state=State)
        authorization_url, state = session.authorization_url(OAuth_authorize_url,access_type="offline", prompt="select_account")
        login_data = {"username": (None,args[1]['username']), "password": (None, args[1]["password"])}
        resp = session.post(url = API_project_url, files=login_data)
        logger.info('用户登录' + "(username:%s；password:%s)" % (args[1]['username'], args[1]["password"]))
        print('<p>测试数据:%s</p>' %args[1])
        # logger.info(authorization_url)
        logger.info('登录重定向URL:%s' %resp.url)
        redirect = session.get(url=authorization_url)
        redirect_url = redirect.url
        # logger.info(redirect_url)
        try:
            tokenInfo = session.fetch_token(OAuth_token_url, client_secret=Client_secret, authorization_response=redirect_url)
            write_txt_Response_data(str(tokenInfo), 'TokenInfo.txt')
            logger.info('用户名密码正确')
            logger.info('身份认证成功' )
        except Exception as e:
            print('<p>身份认证失败： %s</p>' %(str(e)))
            if "err=4001" in resp.url:
                logger.info('用户名不存在')
            elif "err=4002" in resp.url:
                logger.info('密码错误')
            elif "err=4003" in resp.url:
                logger.info('账号过期')
            elif "err=4004" in resp.url:
                logger.info('账号锁定')
            elif "err=4005" in resp.url:
                logger.info('账号禁用')
            elif "err=4006" in resp.url:
                logger.info('密码过期')
            else:
                pass
        resp1 = session.get(url=args[0])
        write_txt_Response_data(str(resp1.text), 'UserInfo.txt')
        if '"code":200' and '"message":"success"' in resp1.text:
            logger.info("API用户登录-Success.")
        elif '"code":4000' and '"message":"no_login"'in resp1.text:
            logger.info("\033[1;35mAPI用户登录-Fail.\033[0m")
        else:
            pass
        return resp1

@ddt
class Test_API_TS_Login_001_OAuth(unittest.TestCase):

    data_list = Get_excel_data(API_testdata_path, API_Sheet9, "API")

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
        clean_txt_Response_data('UserInfo.txt')
        clean_txt_Response_data('TokenInfo.txt')

    def setUp(self):
        logger.info("Test case : %s" % self.__class__.__name__)

    @data(*data_list[sys._getframe().f_code.co_name])
    @unpack
    def test_API_TS_Login_001_OAuth(self,testdata,url,firstURL,attach,hope,number,testNum):
        """
            用户登录
        """
        resp1 = user_OAuthLogin().step(url, testdata)
        self.Test_assert(number,testNum, hope, resp1.text,'in')

    def tearDown(self):
        logger.info("----------------------------------------------------------------")

if __name__ == '__main__':
    unittest.main()