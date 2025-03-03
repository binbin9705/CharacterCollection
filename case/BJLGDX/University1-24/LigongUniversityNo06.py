import pandas as pd, time, logging, colorlog
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNo06(object):
    def __init__(self, one_url,school):
        self.one_url = one_url
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
        self.driver.get(self.one_url)
        counts=self.driver.find_elements(By.XPATH,'//*[@class="column2"]//li')
        print(len(counts))
        for c in counts:
            low_url=self.driver.current_url
            types =c.find_element(By.XPATH,'./../../h3').text
            name = c.find_element(By.XPATH,'.//a').text
            print(name)
            # 进详情
            # c.click()
            self.driver.get(c.find_element(By.XPATH,'.//a').get_attribute("href"))
            time.sleep(0.5)
            photos = self.driver.find_elements(By.XPATH, '//*[@class="article"]//img')
            if len(photos) != 0:
                photo = '\n'.join(map(lambda e: e.get_attribute("src"), photos))
            else:
                photo = ''
            introduces=self.driver.find_elements(By.XPATH,'//*[@class="article"]')
            if len(introduces)!=0:
                introduce = '\n'.join(map(lambda e: e.text, introduces))
                introduce=introduce.replace(' ', '')
            else:
                introduce = ''
             # print(introduce)
            if "专业领域：" in introduce:
                field = introduce.split("专业领域：")[1].split("\n")[0]
            else:
                field = ''
            if "职称：" in introduce:
                title=introduce.split("职称：")[1].split("\n")[0]
            else:
                title=''
            if "电话：" in introduce:
                phone = introduce.split("电话：")[1].split("\n")[0]
            else:
                phone = ''
            if "电子邮箱："in introduce:
                mailbox = introduce.split("电子邮箱：")[1].split("\n")[0]
            elif "Email：" in introduce:
                mailbox = introduce.split("Email：")[1].split("\n")[0]
            else:
                mailbox = ''

            data = {}
            data['姓名'] = name
            data['研究领域'] = field
            data['职称'] = title
            # data['荣誉称号'] = honor
            data['荣誉称号'] = ''
            data['电话'] = phone
            data['邮箱'] = mailbox
            data['简介'] = introduce
            data['照片'] = photo
            data['类型'] = types
            print(data)
            self.ResultList.append(data)
            nuw_url=self.driver.current_url
            if nuw_url!=low_url:
                self.driver.back()
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx',encoding='xlsxwriter')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    one_url ='https://xuteli.bit.edu.cn/szdw/xsds/index.htm'
    #学校
    school='北京理工大学-徐特立学院'
    demo = LigongUniversityNo06(one_url,school)
    demo.start()
