import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class XxXY(object):
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
        nums=[1]
        for n in nums:
            self.driver.find_element(By.LINK_TEXT,str(n)).click()
            counts = self.driver.find_elements(By.XPATH, '//*[@id="main"]/div[2]/div[3]/div[4]/div')
            print(len(counts))
            for c in counts:
                #照片
                photo=c.find_element(By.XPATH,'.//img').get_attribute('src')
                #姓名
                name=c.find_element(By.XPATH,'.//div[2]/div').text
                #研究领域
                field = c.find_element(By.XPATH, './/div[contains(text(),"研究方向")]/following-sibling::*[1]').text
                print(c.find_element(By.XPATH,'.//a').get_attribute('href'))
                self.driver.get(c.find_element(By.XPATH,'.//a').get_attribute('href'))
                #简介
                introduce=self.driver.find_elements(By.XPATH,'//*[@id="prof_intro"]')
                if len(introduce) != 0:
                    introduce = '\n'.join(map(lambda e: e.text, introduce))
                else:
                    introduce=''
                # 邮箱
                mailboxs = self.driver.find_elements(By.XPATH, '//p[contains(text(),"电子邮箱：")]')
                if len(mailboxs) != 0:
                    mailboxs = '\n'.join(map(lambda e: e.text, mailboxs))
                    mailbox = mailboxs.split("电子邮箱：")[1]
                else:
                    mailbox = ""
                # 联系方式
                phones = self.driver.find_elements(By.XPATH, '//p[contains(text(),"电话    ：")]')
                if len(phones) != 0:
                    phones = '\n'.join(map(lambda e: e.text, phones))
                    phone = phones.split("：")[1]
                else:
                    phone = ""
                #荣誉称号
                honor1 = self.driver.find_elements(By.XPATH, '//*[@id="main"]/div[2]/div[11]/div[2][text()[normalize-space()]]')
                if len(honor1)!=0:
                    honor='\n'.join(map(lambda e:e.text,honor1))
                else:
                    honor=''
                data = {}
                data['姓名'] = name
                data['研究领域'] = field
                # data['职称'] = '教授'
                data['职称'] = '客座教授'
                data['荣誉称号'] = honor
                data['电话'] = phone
                data['邮箱'] = mailbox
                data['简介'] = introduce
                data['照片'] = photo
                data['类型'] ='在职教师'
                self.ResultList.append(data)
                print(data)
                self.driver.back()
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    # 在职教师
    # one_url = 'http://info.ruc.edu.cn/jsky/szdw/ajxjgcx/bx/js/index.htm'
    one_url = 'http://info.ruc.edu.cn/jsky/szdw/ajxjgcx/bx/kzjs/index.htm'
    # 学校
    school = '人民大学-信息学院客座教授'
    demo = XxXY(one_url, school)
    demo.start()
