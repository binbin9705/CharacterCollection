import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class qizhidao(object):
    def __init__(self, one_url,school):
        self.one_url = one_url
        # self.two_url = two_url
        # self.three_url = three_url
        # self.four_url = four_url
        self.school=school
        # 表头
        self.title = ['接口分类', '接口中文名', '接口英文名']
        self.ResultList = []  # 最终数据

    def options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")  # 规避监测selenium
        options.add_argument('--start-maximized')  # 全屏运行
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 取消chrome受自动控制提示
        # 关掉浏览器记住密码弹窗
        prefs = {"": ""}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option("prefs", prefs)
        # options.headless=True
        return options

    def isElementPresent(self, by, value):
        try:
            element = self.driver.find_element(by=by, value=value)
        except NoSuchElementException as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True
    def start(self):
        self.driver = webdriver.Chrome(options=self.options())
        time.sleep(1)
        # 在职教师
        self.driver.get(self.one_url)
        time.sleep(1)
        self.driver.find_element(By.NAME,'username').send_keys('hubinbin')
        time.sleep(1)
        self.driver.find_element(By.NAME,'password').send_keys('hbb@0311')
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//span[contains(text(),"登录")]').click()
        time.sleep(3)
        self.driver.find_element(By.XPATH,'//h4[contains(text(),"'+self.school+'")]').click()
        # time.sleep(1)
        counts = self.driver.find_elements(By.XPATH, "//h4[contains(text(),'"+self.school+"')]/../following-sibling::*")
        print(len(counts))
        time.sleep(1)
        for c in range(1, int(len(counts))+1):
            time.sleep(1)
            #标题
            postname=self.driver.find_element(By.XPATH,"//h4[contains(text(),'"+self.school+"')]/../following-sibling::*["+str(c)+"]/span[1]").text
            print(postname)
            #发布时间
            posteglname=self.driver.find_element(By.XPATH,"//h4[contains(text(),'"+self.school+"')]/../following-sibling::*["+str(c)+"]/span[2]").text
            print(posteglname)
            #发布部门
            title=self.school
            data = {}
            data['接口分类'] = title
            data['接口中文名'] = postname
            data['接口英文名'] = posteglname
            self.ResultList.append(data)
            print(data)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        print(self.ResultList)
        df.to_excel('./接口类别-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = 'http://39.106.134.50:9528/'
    #学校
    school='电信定制化接口'
    demo = qizhidao(one_url,school)
    demo.start()
