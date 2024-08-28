from os import environ
from config.ProjectInfo import GUI_project_url,usernameId,passwordId,loginEle,projectTitle,Client_id,Redirect_uri,\
    Scope,State,OAuth_authorize_url,API_project_url,OAuth_token_url,Client_secret
from method.GUI_Action import GUI_Action
from selenium.webdriver.common.by import By
from method.out_log import logger
from requests_oauthlib import OAuth2Session, TokenUpdated


class GUI_Login(GUI_Action):

    def GUI_LoginWeb(self,username,password):
        self.open_url(GUI_project_url)
        self.page_loading()
        self.window_size("最大化")
        action1 = "输入用户名 : "+username
        self.sendKeys_element(By.ID, usernameId,username,action1)
        action2 = "输入密码"
        self.sendKeys_element(By.ID,passwordId,password,action2)
        action3 = "点击登录"
        self.click_element(By.XPATH, loginEle,action3)
        try:
            if self.is_title_contains(projectTitle, timeout=10):
                logger.info("GUI login successfully.")
        except Exception as e:
            logger.error("\033[1;35mGUI login failed : %s.\033[0m" %(str(e)))


class API_Login():

    def API_LoginWeb(self,username,password):
        environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        self.session = OAuth2Session(Client_id, redirect_uri=Redirect_uri,scope=Scope, state=State)
        authorization_url, state = self.session.authorization_url(OAuth_authorize_url)
        data = {"username": (None, username), "password": (None, password)}
        self.session.post(url=API_project_url, files=data)
        redirect = self.session.get(url=authorization_url)
        redirect_url = redirect.url
        tokenInfo = self.session.fetch_token(OAuth_token_url, client_secret=Client_secret,authorization_response=redirect_url)
        resp = self.session.get(url='http://auth.hl.fat/v1.0/oauth2/user')
        try:
            if username in resp.text:
                logger.info("API login successfully.")
        except Exception as e:
            logger.error("\033[1;35mAPI login failed : %s.\033[0m" % (str(e)))
        return tokenInfo, self.session

if __name__ == '__main__':
    pass

