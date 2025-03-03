from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time, requests


class Runmian():
    def __init__(self, driver):
        self.driver = driver

    # 浏览器参数设置
    def options(self):
        option = Options()  # Options类实例化
        # option.add_argument('--incognito')# 无痕模式
        option.add_argument('no-sandbox')  # 以最高权限运行
        option.add_argument('--start-maximized')  # 最大化运行（全屏窗口）设置元素定位比较准确
        option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        # 关闭“chrome正受到自动测试软件的控制”
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option("detach", True)  # 不自动关闭浏览器
        # 关掉浏览器记住密码弹窗
        prefs = {"": ""}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        option.add_experimental_option("prefs", prefs)


        # option = Options()
        #无头模式
        option.add_argument('--headless')
        #设置指定分辨率
        # option.add_argument('window-size=1920x1080')
        option.add_argument('--disable-gpu')
        # option.add_argument('--no-sandbox')
        return option

    # 登录
    def login(self, username, password):
        '''输入用户名和密码,点击登录'''
        # 调用显示等待方法 传入判断可见的值
        self.selp("elementto", "name", "username")
        Runmian(self.driver).input_data("name", "username", username)
        self.selp("elementto", 'name', 'password')
        Runmian(self.driver).input_data('name', 'password', password)
        self.selp("elementto", "class_name", "el-button")
        Runmian(self.driver).click('class_name', 'el-button')

    # def login(self, username, password):
        # '''获取登录接口的token 写入访问的页面'''
        # self.driver.execute_script("localStorage.setItem(arguments[0],arguments[1]);", 'Token', 'Bearer ' +
                                   # Runmian(self.driver).get_token(username, password))
        # self.driver.execute_script("localStorage.setItem(arguments[0],arguments[1]);", 'placeBase',
                                   # '{"code":"320000","createTime":"-","jpCode":"-","jpName":"-","level":2,"name":"江苏省","pCode":"100000","pName":"中国","parentArea":"-","state":"-","type":"-","updateTime":"-"}')
        # time.sleep(1)
    # # 获取token
    # def get_token(self, username, password):
        # url = 'http://ihd.wanvdata.cn/api/login.do'
        # data = {
            # 'username': str(username),
            # 'password': str(password),
            # 'sa_key': 'sa_ihqd'
        # }
        # res = requests.post(url=url, data=data).json()
        # # print(res)
        # return res['jwtToken']

    # 打开网页功能
    def open(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

    # 关闭当前窗口
    def close(self):
        self.driver.close()

    # 退出驱动并关闭所有关联的窗口。
    def quit(self):
        # time.sleep(3)
        self.driver.quit()

    # 定位元素
    def locateElement(self, type, value, num=None):
        el = None
        if type == "id":
            el = self.driver.find_element(By.ID, value)
        if type == "ids":
            el = self.driver.find_elements(By.ID, value)[num]
        elif type == "name":
            el = self.driver.find_element(By.NAME, value)
        elif type == "names":
            el = self.driver.find_elements(By.NAME, value)[num]
        elif type == "class_name":
            el = self.driver.find_element(By.CLASS_NAME, value)
        elif type == "class_names":
            el = self.driver.find_elements(By.CLASS_NAME, value)[num]
        elif type == "tag_name":
            el = self.driver.find_element(By.TAG_NAME, value)
        elif type == "tag_names":
            el = self.driver.find_elements(By.TAG_NAME, value)[num]
        elif type == "link_text":
            el = self.driver.find_element(By.LINK_TEXT, value)
        elif type == "link_texts":
            el = self.driver.find_elements(By.LINK_TEXT, value)[num]
        elif type == "partial_link_text":
            el = self.driver.find_element(By.PARTIAL_LINK_TEXT, value)
        elif type == "partial_link_texts":
            el = self.driver.find_elements(By.PARTIAL_LINK_TEXT, value)[num]
        elif type == "xpath":
            el = self.driver.find_element(By.XPATH, value)
        elif type == "xpaths":
            el = self.driver.find_elements(By.XPATH, value)[num]
        elif type == "css":
            el = self.driver.find_element(By.CSS_SELECTOR, value)
        elif type == "csss":
            el = self.driver.find_elements(By.CSS_SELECTOR, value)[num]
        return el

    # 对定位到元素进行点击
    def click(self, type, value, num=None):
        # 调用locateElement定位元素
        el = self.locateElement(type, value, num)
        # 调用click()进行点击操作
        el.click()

    # 获取元素text文本
    def obtaintest(self, type, value, num=None):
        # 调用locateElement定位元素
        el = self.locateElement(type, value, num)
        # 返回
        return el.text

    # 获取任意元素值
    def obtainvalue(self, valuename, type, value, num=None):
        '''class,title,name'''
        # 调用locateElement定位元素
        el = self.locateElement(type, value, num)
        # 返回
        return el.get_attribute(valuename)

    # 输入
    def input_data(self, type, value, data, num=None):
        # 调用locateElement定位元素
        el = self.locateElement(type, value, num)
        # 调用send_keys进行输入
        el.send_keys(data)

    # 切换title页
    def switch_window_by_title(self, title):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if self.driver.title.__contains__(title):
                break

    # 切换frame
    def switch_window_by_frame(self, frame):
        self.driver.switch_to.frame(frame)

    # 显示等待
    def selp(self, category, type=None, value=None, titlevalue=None):
        if category == "elementdwd":
            # 等待10s，等待过程中如果定位到元素，就直接执行后续的代码，反之等待10s后报错误信息//适用于输入框
            WebDriverWait(self.driver, 10).until(EC.visibility_of(self.locateElement(type, value)))
        elif category == "titleis":
            # 等待10s,等待过程中判断网页标题是否是输入title名称
            WebDriverWait(self.driver, 10).until(EC.title_is(titlevalue))
        elif category == "elementkj":
            if type == "css":
                # 等待10s,等待过程中判断某个元素是否可见. 可见表明元素非隐藏，而且元素的宽和高都不等于0//适用于可在页面上肉眼能看到的内容
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, value)))
            elif type == 'class_name':
                # 等待10s,等待过程中判断某个元素是否可见. 可见表明元素非隐藏，而且元素的宽和高都不等于0"
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, value)))
            elif type == 'link_text':
                # 等待10s,等待过程中判断某个元素是否可见. 可见表明元素非隐藏，而且元素的宽和高都不等于0"
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, value)))
            elif type == 'id':
                # 等待10s,等待过程中判断某个元素是否可见. 可见表明元素非隐藏，而且元素的宽和高都不等于0"
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, value)))
