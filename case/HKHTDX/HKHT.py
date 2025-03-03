import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup

class CharacterCollection(object):
    def __init__(self, one_url, two_url, three_url,four_url,school):
        self.one_url = one_url
        self.two_url = two_url
        # self.three_url = three_url
        # self.four_url = four_url
        self.school=school
        # 表头
        self.title = ['姓名', '研究领域', '职称', '荣誉称号', '电话','邮箱','简介','照片','类型']
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
        # 两院院士
        self.driver.get(self.one_url)
        for x in range(1,5):
            if x!=1:
                wei = 'p_next_d p_fun_d'
                whole = self.isElementPresent(by=By.CLASS_NAME, value=wei)
                if whole != True:
                    self.driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div/div/div/span[2]/span[7]/a').click()
                else:
                    pass
            # 职称、类型
            title = self.driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[1]/div/h4/span').text
            # 获取每个li标签
            elements = self.driver.find_elements(By.XPATH, '/html/body/div[6]/div[3]/div/div/ul/li')
            for x in elements:
                x.click()
                #姓名
                name=x.find_element(By.XPATH,'./div/div/div[2]/h4').text
                p_s = x.find_elements(By.XPATH,'.//div[@class="scrolltext"]//p[normalize-space()]')
                # 研究领域、荣誉称号、简介
                area='\n'.join(map(lambda e: e.text, p_s))
                photo = x.find_element(By.XPATH,'./div/div/div[2]/div/div[2]/img').get_attribute("src")
                data = {}
                data['姓名'] = name
                data['研究领域'] = area
                data['职称'] = title
                data['荣誉称号'] = area
                data['电话'] = ''
                data['邮箱'] = ''
                data['简介'] = area
                data['照片'] = photo
                data['类型'] = title
                self.ResultList.append(data)
                print(data)
                x.find_element(By.XPATH,'./div/div/div[1]').click()
                continue
        self.driver.quit()
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #两院院士
    one_url = 'https://www.buaa.edu.cn/rcpy/szdw/lyys.htm'
    #国家级教学名师
    two_url = 'https://www.buaa.edu.cn/rcpy/szdw/gjjjxms1.htm'
    # 发展中国家科学院院士
    three_url = 'https://www.pku.edu.cn/developing_countries.html'
    # 国家级教学名师
    four_url = 'https://www.pku.edu.cn/national_famous_teacher.html'
    #学校
    school='航空航天'
    demo = CharacterCollection(one_url, two_url, three_url,four_url,school)
    demo.start()
