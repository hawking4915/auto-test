#coding=utf-8

from random import randint
from time import sleep, strftime
from warnings import simplefilter
from pytesseract import image_to_string
from method.out_log import logger
from selenium.webdriver import ChromeOptions,Chrome,FirefoxOptions,Firefox,IeOptions,Ie
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait        # 用于处理元素等待
from selenium.webdriver.common.action_chains import ActionChains  # 处理鼠标事件
from selenium.webdriver.common.keys import Keys                   # 处理键盘事件
from selenium.webdriver.support.select import Select              # 用于处理下拉框
from selenium.common.exceptions import *                          # 用于处理异常
from PIL import Image, ImageEnhance
from pytesser.IdentifyImage import identifyImage
from lxml.etree import HTML,tostring
from bs4 import BeautifulSoup
from method.try_except import try_except

# -----------------------------------------------------------
#     author：wangshinan
#     description：定义一个获取能够操作界面元素的self.driver对象
#     param：1、browser_type  浏览器类型
#     remarks：浏览器类型：chrome7.5/'谷歌7.5'   chrome7.7/'谷歌7.7'  'firefox'/'火狐'   'IE'
#               下载好浏览器驱动同意放置self.driver文件夹（self.driver文件夹位置随意）
#             1.将浏览器驱动放置在本地python路径下，使用方法：self.self.driver = webdriver.Chrome()
#             2.在commonConfig文件夹下配置浏览器驱动绝对路径，使用方法：
#             self.self.driver = webdriver.Chrome(commonConfig.chrome)
#             3.浏览器为火狐/IE，与Chrome同理，使用方法：self.self.driver = webdriver.firefox() /
#             self.self.driver = webdriver.ie()
#
#              浏览器驱动chromeself.driver1.exe   仅支持chrome版本75；
#              chromeself.driver2.exe   支持chrome版本77
# -----------------------------------------------------------

def open_driver(browser_type,path):
    simplefilter('ignore', DeprecationWarning)
    try:
        if browser_type == 'chrome' or browser_type == '谷歌':
            chrome_option = ChromeOptions()
            chrome_option.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
            chrome_option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
            # chrome_option.add_argument('disable-infobars')#自动化测试时，启动浏览器隐藏‘Chrome正在受到自动软件的控制’信息栏
            # chrome_option.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
            # chrome_option.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
            chrome_option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
            driver_path = path +  '\chromedriver.exe'
            driver = Chrome(executable_path=driver_path)
            # driver = webdriver.Chrome(executable_path=driver_path,chrome_options =chrome_option)
            logger.info("浏览器 : %s." % browser_type)
            return driver
        elif browser_type == 'firefox' or browser_type == '火狐':
            firefox_option = FirefoxOptions()
            firefox_option.add_argument('--headless')
            firefox_option.add_argument('--disable-gpu')
            # firefox_option.add_argument('disable-infobars')
            # firefox_option.add_argument('window-size=1920x3000')
            # firefox_option.add_argument('--hide-scrollbars')
            # firefox_option.add_argument('blink-settings=imagesEnabled=false')
            driver_path = path + '\geckodriver.exe'
            driver = Firefox(executable_path=driver_path,firefox_options=firefox_option)
            logger.info("浏览器 : %s." % browser_type)
            return driver
        elif browser_type == 'IE' or browser_type == 'Ie':#os.path.join(os.getcwd()
            IE_option = IeOptions()
            IE_option.add_argument('--headless')
            IE_option.add_argument('--disable-gpu')
            # IE_option.add_argument('disable-infobars')
            # IE_option.add_argument('window-size=1920x3000')
            # IE_option.add_argument('--hide-scrollbars')
            # IE_option.add_argument('blink-settings=imagesEnabled=false')
            driver_path = path + '\IEDriverServer.exe'
            driver = Ie(executable_path=driver_path,ie_options=IE_option)
            logger.info("浏览器 : %s." % browser_type)
            return driver
        else:
            logger.info("\033[1;35m注意：Not found this browser, You can enter 'chrome','firefox' or 'IE'\033[0m")
    except Exception as e:
        logger.error("\033[1;35m%s.\033[0m" % (str(e)))

# -----------------------------------------------------------
#     author：wangshinan
#     description：关闭self.driver和所有窗口
#     param：
#     remarks：
# -----------------------------------------------------------

def quit(driver):
    # logger.info("关闭self.driver和所有窗口")
    driver.quit()

#继承object对象，会拥有好多可操作对象，都是类中的高级特性
#不继承object对象，仅有__doc__ , module 和 自定义的变量
class GUI_Action(object):

    def __init__(self, driver):
        self.driver = driver
# -----------------------------------------------------------
#     author：wangshinan
#     description：打开网页
#     param：
#     remarks：
# -----------------------------------------------------------\

    def open_url(self,url):
        logger.info("打开网页 : "+url)
        self.driver.get(url)

# -----------------------------------------------------------
#     author：wangshinan
#     description：获取当前窗口的title
#     param：
#     remarks：方法二：title = UiAutoTestCase.parse(self.driver.page_source, '//title/text()')[0]
# -----------------------------------------------------------
    
    def get_browsers_title(self):
        logger.info("获取当前窗口的title：%s" %self.driver.title)
        return self.driver.title

# -----------------------------------------------------------
#     author：wangshinan
#     description：窗口最大化/最小化
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def window_size(self,size):
        if size == "最大化":
            logger.info("窗口最大化")
            self.driver.maximize_window()
        elif size == "最小化":
            logger.info("窗口最小化")
            self.driver.minimize_window()
        else:
            pass

# -----------------------------------------------------------
#     author：wangshinan
#     description：页面加载
#     param：
#     remarks：
# -----------------------------------------------------------\
    
    def page_loading(self,timeout = 10):
        logger.info("页面加载中......")
        self.driver.set_page_load_timeout(timeout)
        self.driver.implicitly_wait(timeout)

# -----------------------------------------------------------
#     author：wangshinan
#     description：获取当前页面url
#     param：
#     remarks：
# -----------------------------------------------------------\
    
    def get_current_url(self):
        logger.info("获取当前页面URL：%s" %self.driver.current_url)
        return self.driver.current_url

# -----------------------------------------------------------
#     author：wangshinan
#     description：显示等待定位元素-定位元素
#     param：1、by  定位元素方法
#            2、value  元素值
#            3、timeout  超时时间
#     remarks：判断元素是否定位到（元素不一定是可见）
#           只要一个符合条件的元素加载出来就通过
#           如果定位到返回Element，未定位到返回FALSE
#           当我们不关心元素是否可见，只关心元素是否存在在页面中:presence_of_element_located
#           当我们需要找到元素，并且该元素也可见：visibility_of_element_located
# -----------------------------------------------------------
    
    def wait_for_element_find(self, by, value, timeout=10):
        # 第一种显示等待的实现方法
        # for i in range(timeout):
        #     try:
        #         cls.self.driver.find_element(by, value)
        #         return True
        #     except NoSuchElementException:
        #         time.sleep(1)
        # return False

        # 第二种显示等待的实现方法
        try:
            element = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((by, value)))
            # WebDriverWait(cls.self.driver, timeout).until(lambda dr: dr.find_element(by, value))
        except Exception as e:
            logger.error("\033[1;35mFind element failed :  %s.\033[0m" %(value))
            return False
        else:
            return element

# -----------------------------------------------------------
#     author：wangshinan
#     description：显示等待定位元素-定位一组元素
#     param：1、(locator) 多组元素((by,value),(by,value)...)
#            3、timeout  超时时间
#     remarks：必须所有符合条件的元素都加载出来才行
# -----------------------------------------------------------
    
    def wait_for_elements_find(self, by, value, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_all_elements_located((by, value)))
        except Exception as e:
            logger.error("\033[1;35mFind element failed :  %s.\033[0m" %(value))
            return False
        else:
            print()
            return elements

# -----------------------------------------------------------
#     author：wangshinan
#     description：判断元素可见，可见返回元素本身，不可见返回FALSE
#                  可见代表元素非隐藏，并且元素的宽和高都不等于0
#     param：1、by  定位元素方法
#            2、value  元素值
#     remarks：当我们需要找到元素，并且该元素也可见。
# -----------------------------------------------------------
    
    def is_visibility(self, by,value, timeout=10):
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located((by, value)))
        except Exception as e:
            logger.error("\033[1;35m该元素未找到 : %s.\033[0m" %value)
            return False
        else:
            return result

# -----------------------------------------------------------
#     author：wangshinan
#     description：判断元素不可见或不存在于dom树，不可见，未找到元素返回True
#     param：1、by  定位元素方法
#            2、value  元素值
#     remarks：
# -----------------------------------------------------------
    
    def is_invisibility(self,  by,value, timeout=10):
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(EC.invisibility_of_element_located((by, value)))
        except Exception as e:
            logger.error("\033[1;35m该元素未找到 : %s.\033[0m" % value)
            return True
        else:
            return result


# -----------------------------------------------------------
#     author：wangshinan
#     description：判断元素是否显示，结果为一个布尔值，True或False
#     param：1、by  定位元素方法
#            2、value  元素值
#     remarks：注意self.wait_for_element_find(by, value)中
#             返回值'WebElement' object has no attribute 'is_display'
# -----------------------------------------------------------
    
    def is_display(self, by, value):
        try:
            result = self.driver.find_element(by, value).is_displayed()
        except Exception as e:
            logger.error("\033[1;35m该元素未显示在当前页面: %s.\033[0m" %value)
            return False
        else:
            return result
# -----------------------------------------------------------
#     author：wangshinan
#     description：点击元素
#     param：1、by  定位元素方法
#            2、value  元素值
#            3、timeout  超时时间
#     remarks：
# -----------------------------------------------------------

    def click_element(self,by, value,action) -> object:
        try:
            element = self.wait_for_element_find(by, value)
            logger.info(action)
            element.click()
            self.time_wait(1)
        except Exception as e:
            logger.error("\033[1;35mClick failed : %s.\033[0m" %value)

# -----------------------------------------------------------
#     author：wangshinan
#     description：元素赋值
#     param：1、by  定位元素方法
#            2、value  元素值
#            3、timeout  超时时间
#            4、keys  赋值参数
#     remarks：
# -----------------------------------------------------------
    
    def sendKeys_element(self,by, value, keys,action):
        try:
            element = self.wait_for_element_find(by, value)
            logger.info(action)
            element.click()
            element.clear()
            element.send_keys(keys)
        except Exception as e:
            logger.error("\033[1;35mSendkeys failed : %s.\033[0m" %value)

# -----------------------------------------------------------
#     author：wangshinan
#     description：判断某个元素中是否 包含 了预期的字符串-判断元素的text
#     param：1、text
#            2、by  定位元素方法:
#            3、value  元素值
#     remarks：WebDriverWait(self.driver,10).until(EC.text_to_be_present_in_element((By.XPATH,"//*[@id='u1']/a[8]"),u'设置'))
# -----------------------------------------------------------
    
    def is_text_in_element(self, text, by, value, timeout=10):
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(EC.text_to_be_present_in_element((by, value), text))
            logger.info("该文本存在 : %s." % text)
        except Exception as e:
            logger.error("\033[1;35m该文本不存在 : %s.\033[0m" %text)
            return False
        else:
            return result

# -----------------------------------------------------------
#     author：wangshinan
#     description：判断某个元素的属性值中是否 包含 了预期的字符串-一个判断元素的value
#     param：1、text
#            2、by  定位元素方法
#            3、value  元素值
#     remarks：WebDriverWait(self.driver,10).until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR,'#su'),u'百度一下'))
# -----------------------------------------------------------
    
    def is_text_in_element_value(self, text, by, value, timeout=10):
        try:
            result = WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element_value((by, value), text))
        except Exception as e:
            logger.error("\033[1;35m该元素的属性值不存在 : %s.\033[0m" % text)
            return False
        else:
            return result

# -----------------------------------------------------------
#     author：wangshinan
#     description：GUI登录验证码处理
#     param：1、by  定位元素方法
#            2、value  元素值
#     remarks：
# -----------------------------------------------------------
    
    def GUI_Code(self, by, value):
        try:
            code,judge= self.wait_for_element_find(by, value)  #judge:True/False
            value = identifyImage(self.driver, code, 'vCode.jpg')
            code.send_keys(value)
            return True
        except Exception as e:
            return False

# -----------------------------------------------------------
#     author：wangshinan
#     description：:判断当前页面的title是否完全等于（==）预期字符串，返回是布尔值
#     param：1、title  网页title
#     remarks：result:True/False
# -----------------------------------------------------------
    
    def is_title(self, title, timeout=10):
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_is(title))
        return result

# -----------------------------------------------------------
#     author：wangshinan
#     description：判断当前页面的title是否包含预期字符串，返回布尔值
#     param：1、title  网页title
#     remarks：result:True/False
# -----------------------------------------------------------
    
    def is_title_contains(self, title, timeout=10):
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))
        return result

# -----------------------------------------------------------
#     author：wangshinan
#     description：随机等待3-10s
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def random_sleep(self):
        t = randint(3, 10)
        # logger.info("Random waiting  %s s" %t)
        sleep(t)

# -----------------------------------------------------------
#     author：wangshinan
#     description：强制等待时间
#     param：1、timeout  等待时间
#     remarks：
# -----------------------------------------------------------
    
    def time_wait(self,timout = 3):
        # logger.info("Waiting %s s " %timout)
        sleep(timout)

# -----------------------------------------------------------
#     author：wangshinan
#     description：判断元素是否被选中
#     param：1、by  定位元素方法
#           2、value  元素值
#     remarks：
# -----------------------------------------------------------
    
    def is_select(self, by, value, timeout=10):
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_to_be_selected((by, value)))
        return result

# -----------------------------------------------------------
#     author：wangshinan
#     description：判断元素的状态
#     param：1、by  定位元素方法
#           2、value  元素值
#     remarks：
# -----------------------------------------------------------
    
    def is_select_be(self, by, value, timeout=10, selected=True):
        return WebDriverWait(self.driver, timeout, 1).until(EC.element_located_selection_state_to_be((by, value), selected))

# -----------------------------------------------------------
#     author：wangshinan
#     description：判断页面有无alert弹出框，有alert返回alert，无alert返回FALSE
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def is_alert_present(self, timeout=20):
        try:
            alert = WebDriverWait(self.driver, timeout, 1).until(EC.alert_is_present())
        except Exception as e:
            logger.error("\033[1;35mNo  Alert  Present : %s.\033[0m" % (str(e)))
            return False
        else:
            return alert

# -----------------------------------------------------------
#     author：wangshinan
#     description：alert弹出框_点击确认
#     param：
#     remarks：
# -----------------------------------------------------------

    def alert_accept(self,driver):
        try:
            if self.is_alert_present():
                alert = driver.switch_to.alert
                alert.accept()
                logger.info("No")
        except Exception as e:
            logger.error("\033[1;35maccept_Fail: %s.\033[0m" % (str(e)))



# -----------------------------------------------------------
#     author：wangshinan
#     description：判断元素是否可以点击，可以点击返回本身，不可点击返回FALSE
#     param：1、by  定位元素方法
#            2、value  元素值
#     remarks：
# -----------------------------------------------------------
    
    def is_clickable(self,  by,value, timeout=10):
        return WebDriverWait(self.driver, timeout, 1).until(EC.element_to_be_clickable((by, value)))

# -----------------------------------------------------------
#     author：wangshinan
#     description：判断元素是否定位到（元素不一定是可见），如果定位到返回Element，未定位到返回FALSE
#     param：1、by  定位元素方法
#            2、value  元素值
#     remarks：
# -----------------------------------------------------------
    
    def is_located(self,  by,value, timeout=10):
        return WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((by, value)))

# -----------------------------------------------------------
#     author：wangshinan
#     description：鼠标悬停操作
#     param：1、by  定位元素方法
#            2、value  元素值
#     remarks：
# -----------------------------------------------------------\
    
    def move_is_element(self,by,value):
        element = self.wait_for_element_find( by, value)
        ActionChains(self.driver).move_to_element(element).perform()

# -----------------------------------------------------------
#     author：wangshinan
#     description：鼠标双击操作
#     param：1、by  定位元素方法
#            2、value  元素值
#     remarks：
# -----------------------------------------------------------\

    def doubleClick_is_element(self, by, value):
        element = self.wait_for_element_find(by, value)
        ActionChains(self.driver).double_click(element).perform()

# -----------------------------------------------------------
#     author：wangshinan
#     description：鼠标拖动操作
#     param：1、by  定位元素方法
#            2、value  元素值
#     remarks：
# -----------------------------------------------------------\

    def drag_is_element(self, by, value):
        element = self.wait_for_element_find(by, value)  # 定位元素的原位置
        target = self.wait_for_element_find(by, value)  # 定位元素要移动到的目标位置
        ActionChains(self.driver).drag_and_drop(element, target).perform()  # 拖动

# -----------------------------------------------------------
#     author：wangshinan
#     description：键盘回车键操作
#     param：1、by  定位元素方法
#            2、value  元素值
#     remarks：
# -----------------------------------------------------------\

    def ENTER(self, by, value,action):
        element = self.wait_for_element_find(by, value)
        element.send_keys(Keys.ENTER)
        logger.info(action)

# -----------------------------------------------------------
#     author：wangshinan
#     description：键盘回删键操作
#     param：1、by  定位元素方法
#            2、value  元素值
#     remarks：
# -----------------------------------------------------------\

    def BACK_SPACE(self, by, value):
        element = self.wait_for_element_find(by, value)
        element.send_keys(Keys.BACK_SPACE)

# -----------------------------------------------------------
#     author：wangshinan
#     description：键盘空格键操作
#     param：1、by  定位元素方法
#            2、value  元素值
#     remarks：
# -----------------------------------------------------------\

    def SPACE(self, by, value):
        element = self.wait_for_element_find(by, value)
        element.send_keys(Keys.SPACE)

# -----------------------------------------------------------
#     author：wangshinan
#     description：键盘ctrl+A/C/V/X  全选/复制/粘贴/剪切操作
#     param：1、by  定位元素方法
#            2、value  元素值
#            3、key   A/C/V/X  例如：element.send_keys(Keys.CONTROL,‘a’)
#     remarks：
# -----------------------------------------------------------\

    def ctrl_A(self, by, value,key):
        element = self.wait_for_element_find(by, value)
        element.send_keys(Keys.CONTROL,key)

# -----------------------------------------------------------
#     author：wangshinan
#     description：返回到旧的窗口
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def back(self):
        logger.info("Page back.")
        self.driver.back()

# -----------------------------------------------------------
#     author：wangshinan
#     description：页面刷新
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def refresh(self):
        logger.info("Page refresh.")
        self.driver.refresh()

# -----------------------------------------------------------
#     author：wangshinan
#     description：前进到新窗口
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def forward(self):
        logger.info("Page advance.")
        self.driver.forward()

# -----------------------------------------------------------
#     author：wangshinan
#     description：关闭窗口
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def close(self):
        # logger.info("关闭当前窗口")
        self.driver.close()

# -----------------------------------------------------------
#     author：wangshinan
#     description：获取一个元素文本内容
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def get_text(self, by, value):
        try:
            element=self.wait_for_element_find(by, value)
        except Exception as e:
            logger.error("\033[1;35m获取元素文本内容_Fail.\033[0m" )
            return False
        else:
            return element.text

# -----------------------------------------------------------
#     author：wangshinan
#     description：获取一组元素文本内容
#     param：
#     remarks：
# -----------------------------------------------------------

    def get_texts(self, by, value):
        try:
            elements = self.wait_for_elements_find(by, value)
            texts=[]
            for i in elements:
                text = i.text
                texts.append(text)
        except Exception as e:
            logger.error("\033[1;35m获取一组元素文本内容_Fail.\033[0m")
            return False
        else:
            return texts

# -----------------------------------------------------------
#     author：wangshinan
#     description：获取浏览器错误日志级别
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def get_browser_log_level(self):
        lists = self.driver.get_log('browser')
        list_value = []
        if lists.__len__() != 0:
            for dicts in lists:
                for key, value in dicts.items():
                    list_value.append(value)
        if 'SEVERE' in list_value:
            return "SEVERE"
        elif 'WARNING' in list_value:
            return "WARNING"
        return "SUCCESS"

# -----------------------------------------------------------
#     author：wangshinan
#     description：获取一组元素个数
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def get_elementNumber(self, by, value):
        elements= self.wait_for_elements_find(by, value)
        number=len(elements)
        return str(number)

# -----------------------------------------------------------
#     author：wangshinan
#     description：获取元素个数
#     param：
#     remarks：
# -----------------------------------------------------------

    def get_attribute(self, by, value, name, action):
        element = self.wait_for_element_find(by, value)
        logger.info(action)
        return element.get_attribute(name)

# -----------------------------------------------------------
#     author：wangshinan
#     description：异常自动截图
#     param：
#     remarks：
# -----------------------------------------------------------

    def get_screen_as_file(self, func):
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except:
                self.screen()
                raise
        return inner

# -----------------------------------------------------------
#     author：wangshinan
#     description：浏览器页面截图
#     param：
#     remarks：
# -----------------------------------------------------------

    def screen(self):
        nowtime = strftime("%Y%m%d_%H%M%S")
        self.driver.get_screenshot_as_file("%s.png" % nowtime)

# -----------------------------------------------------------
#     author：wangshinan
#     description：执行js
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def js_execute(self, js):
        return self.driver.execute_script(js)

# -----------------------------------------------------------
#     author：wangshinan
#     description：聚焦元素
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def js_fours_element(self,by, value):
        element =self.wait_for_element_find(by, value)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

# -----------------------------------------------------------
#     author：wangshinan
#     description：滑动到页面顶部
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def js_scroll_top(self):
        logger.info("滑动到页面顶部")
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

# -----------------------------------------------------------
#     author：wangshinan
#     description：滑动到页面底部
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def js_scroll_end(self):
        logger.info("滑动到页面底部")
        js = "window.scrollTo(0, document.body.scrollHeight)"
        self.driver.execute_script(js)

# -----------------------------------------------------------
#     author：wangshinan
#     description：下拉选择框:通过所有index，0开始,定位元素
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def select_by_index(self, by, value, index):
        # 定位下拉框
        element=self.wait_for_element_find(by, value)
        Select(element).select_by_index(index)

# -----------------------------------------------------------
#     author：wangshinan
#     description：下拉选择框:通过value定位元素
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def select_by_value(self, by, value, value1):
        # 定位下拉框
        element =self.wait_for_element_find(by,value)
        logger.info(element)
        Select(element).select_by_value(value1)
        return element

# -----------------------------------------------------------
#     author：wangshinan
#     description：下拉选择框:通过text定位元素
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def select_by_text(self, by, value, text,action):
        # 定位下拉框
        element =self.wait_for_element_find(by, value)
        Select(element).select_by_visible_text(text)
        logger.info(action)


# -----------------------------------------------------------
#     author：wangshinan
#     description：获取图片验证码
#     param：
#     remarks：
# -----------------------------------------------------------
    
    def get_verify_code(self,by, value):
        # 验证码图片保存地址
        screenImg = "G:/TianShu/verifyCode/verifyCode.png"
        # 浏览器页面截图
        self.driver.get_screenshot_as_file(screenImg)

        # 定位验证码大小
        location = self.wait_for_element_find(by, value).location
        size = self.wait_for_element_find(by, value).size

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        # 从文件读取截图，截取验证码位置再次保存
        img = Image.open(screenImg).crop((left, top, right, bottom))
        img.convert('L')  # 转换模式：L|RGB
        img = ImageEnhance.Contrast(img)  # 增加对比度
        img = img.enhance(2.0)  # 增加饱和度
        img.save(screenImg)

        # 再次读取验证码
        img = Image.open(screenImg)
        sleep(1)
        code = image_to_string(img)
        return code

#-----------------------------------------------------------
#    author：yinchao
#    description：页面跳转
#    param：self.driver浏览器实例化对象
#    remarks：
#-----------------------------------------------------------
    
    def JumpToProjectSys(self,by,value,action):
        nowhandle = self.driver.current_window_handle #获得当前句柄
        self.click_element(by,value,action) #链接位置（点击之后打开新窗口）
        allhandle = self.driver.window_handles #获得所有句柄
        for handle in allhandle:
            if handle != nowhandle:
                self.driver.switch_to.window(handle)


# -----------------------------------------------------------
#     author：wangshinan
#     description：通过xpath获取html页面部分内容(爬虫)
#     param：1、html    html页面代码
#           2、xpath   想要获取内容的xpath
#     remarks：此处html可为resp.text或者resp.content
#              resp.text返回的是Unicode型也就是字符串的数据。
#              resp.content返回的是bytes型也就是二进制的数据。
# -----------------------------------------------------------
    
    def getHtmlContent_ByXpath(html,xpath):
        #方法一：
        # 1、etree.HTML(): 解析HTML页面，调用HTML类进行初始化，构造一个XPath解析对象；
        # HTML文本中的最后一个li节点是没有闭合的，但是etree.HTML模块可以自动修正HTML文本。
        # 2、etree.tostring()：对'lxml.etree._Element'进行处理，输出修正后的HTML代码，类型是bytes，
        # 不可以进行编码，需转换成字符串，使用代码.decode()将bytes型转换为str型。
        # 3、变量Ele的类型：'lxml.etree._Element'
        # 4、.xpath(xpath)结果是list类型，.xpath(xpath)[下标]结果是'lxml.etree._Element'类型
        #解析HTML页面还可以用BeautifulSoup(html, "lxml")
        #BeautifulSoup类似 jQuery的选择器，通过 id、css选择器和标签来查找元素，lxml主要通过 html节点的嵌套关系来查找元素
        El = HTML(html)
        Ele0 = El.xpath(xpath)
        #获取目标行
        #str通过(encode)转为bytes，bytes通过(decode)转为str
        #写循环是为了保证查出来的结果有多个时也不会出错
        list= []
        for Ele in Ele0:
            Ele1 = tostring(Ele, encoding = "utf-8", pretty_print = True,method='html').decode('utf-8')
        #Ele1字符串:<input type="hidden" name="lt" value="LT-539016-ZXxgEI0G1Zqv94zEmPcVXRmi47v4qJ-sso.cserver">
            list.append(Ele1)
        return list
        # # 方法二：
        # # fromstring()将bytes/字符串格式化成et对象，tostring()将et对象转回bytes格式
        # Ele = html.fromstring(html).xpath(xpath)[0]
        # Ele1 = html.tostring(Ele).decode('utf-8')
        # return Ele1


if __name__ == '__main__':
    pass
