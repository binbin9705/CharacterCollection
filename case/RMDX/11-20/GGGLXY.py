import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import re


class GGGLXY(object):
    def __init__(self, one_url, school):
        self.one_url = one_url
        self.school = school
        # 表头
        self.title = ['姓名', '研究领域', '职称', '荣誉称号', '电话', '邮箱', '简介', '照片', '类型']
        self.ResultList = []  # 最终数据

    def options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")  # 规避监测selenium
        options.add_argument('--start-maximized')  # 全屏运行
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 不显示chrome受自动控制提示
        # 关掉浏览器记住密码弹窗
        prefs = {"": ""}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option("prefs", prefs)
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
        self.driver.get(self.one_url)
        counts = self.driver.find_elements(By.XPATH,
                                           '/html/body/div[3]/div[2]/div[2]/div[3]/div/div/ul/table/tbody//tr')
        print(len(counts))
        for c in counts[52:55]:
            # 名字
            name = c.find_element(By.XPATH, './/center').text
            print(name)
            # 照片
            photo = c.find_element(By.XPATH, './/img[@src]').get_attribute("src")
            link = c.find_element(By.XPATH, './/a[1]').get_attribute('href')
            print(link)
            self.driver.get(link)
            # 职称
            titles = self.driver.find_elements(By.XPATH,'//*[@id="nbsp"]/table/tbody/tr[1]/td[3]/table/tbody/tr[2]/td[4]')
            if len(titles) != 0:
                title = '\n'.join(map(lambda e: e.text, titles))
            else:
                title = ''
            # 简介
            introduces = self.driver.find_elements(By.XPATH,'//*[@id="nbsp"]/table/tbody/tr[not(@class) or @class!="firstRow"]')
            introduce = '\n'.join(map(lambda e: e.text, introduces))
            introduce = introduce.strip()
            # 研究领域
            fiellds1 = self.driver.find_elements(By.XPATH, "//strong[contains(text(),'研究专长')]")
            print(len(fiellds1))
            if len(fiellds1) != 0:
                fiellds1 = self.driver.find_elements(By.XPATH,
                                                    '//strong[contains(text(),"研究专长")]/../../../../following-sibling::*[1]')
                field = '\n'.join(map(lambda e: e.text, fiellds1))
            else:
                fiellds2 = self.driver.find_elements(By.XPATH, "//p[contains(text(),'研究专长')]")
                if len(fiellds2) != 0:
                    fiellds2 = self.driver.find_elements(By.XPATH,
                                                        '//p[contains(text(),"研究专长")]/../../.././following-sibling::*[1]//td')
                    field = '\n'.join(map(lambda e: e.text, fiellds2))
                else:
                    field = ''
            # print(field)

            # 邮箱
            mailboxs = self.driver.find_elements(By.XPATH,
                                                 '//*[@id="nbsp"]/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td[2]')
            if len(mailboxs) != 0:
                mailbox = '\n'.join(map(lambda e: e.text, mailboxs))
            else:
                mailbox = ''
            # 联系方式
            phones = self.driver.find_elements(By.XPATH,
                                               '//*[@id="nbsp"]/table/tbody/tr[1]/td[3]/table/tbody/tr[4]/td[4]')
            if len(phones) != 0:
                phone = '\n'.join(map(lambda e: e.text, phones))
            else:
                phone = ''
            honor = ''
            data = {}
            data['姓名'] = name
            data['研究领域'] = field
            data['职称'] = title
            data['荣誉称号'] = honor
            data['电话'] = phone
            data['邮箱'] = mailbox
            data['简介'] = introduce
            data['照片'] = photo
            data['类型'] = types
            self.ResultList.append(data)
            print(data)
            self.driver.back()
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    # 全职教师
    one_url = 'http://spap.ruc.edu.cn/jytd/qzjs/index.htm'
    types = '全职教师'
    # 学校
    school = '人民大学-公共管理学院'
    demo = GGGLXY(one_url, school)
    demo.start()
