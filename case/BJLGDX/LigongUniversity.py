import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNO01(object):
    def __init__(self, one_url,school):
        self.one_url = one_url
        # self.two_url = two_url
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

    def start(self):
        self.driver = webdriver.Chrome(options=self.options())
        # 在职教师
        self.driver.get(self.one_url)
        conuts=self.driver.find_elements(By.XPATH,'//div[@class="leaderList"]//li')
        for c in conuts:
            name=c.find_element(By.XPATH,'.//font').text
            print(name)
            title=c.find_element(By.XPATH,'.//span').text
            # print(title)
            photo=c.find_element(By.XPATH,'.//img').get_attribute("src")
            #进详情
            c.find_element(By.XPATH, './/font').click()
            introduces=self.driver.find_elements(By.XPATH,'//div[@class="articleTitle02"]/following-sibling::*[1]')
            introduce='\n'.join(map(lambda e:e.text,introduces))
            data = {}
            data['姓名'] = name
            # data['研究领域'] = field
            data['研究领域'] = ''
            data['职称'] = title
            # data['荣誉称号'] = honor
            data['荣誉称号'] = ''
            data['电话'] = ''
            # data['电话'] = phone
            # data['邮箱'] = mailbox
            data['邮箱'] = ''
            data['简介'] = introduce
            data['照片'] = photo
            # data['类型'] = types
            data['类型'] = '部分两院院士'
            print(data)
            self.ResultList.append(data)
            self.driver.back()
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = 'https://renshichu.bit.edu.cn/gbszdw/gblyys/index.htm'
    #学校
    school='北京理工大学'
    demo = LigongUniversityNO01(one_url,school)
    demo.start()
