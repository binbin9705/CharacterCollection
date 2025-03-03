import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNo04(object):
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
        links=[
            'https://smt.bit.edu.cn/szdw/jsml/bssds/index.htm',
            'https://smt.bit.edu.cn/szdw/jsml/sssds/index.htm'
        ]
        for link in links:
            self.driver.get(link)
            counts=self.driver.find_elements(By.XPATH,'//*[@class="tabs"]//li')
            print(len(counts))
            for c in counts:
                name=c.find_element(By.XPATH,".//p").text
                photo=c.find_element(By.XPATH,'.//img').get_attribute("src")
                #进详情
                c.find_element(By.XPATH,'.//a').click()
                fields=self.driver.find_elements(By.XPATH,'//*[contains(text(),"研究领域")]/../following-sibling::*[1]')
                if len(fields)!=0:
                    field='\n'.join(map(lambda e:e.text,fields))
                else:
                    field=''
                titles=self.driver.find_elements(By.XPATH,'//div[@class="perRtop"]//*[@class="gp-f16"]')
                if len(titles)!=0:
                    title = '\n'.join(map(lambda e: e.text, titles))
                else:
                    title = ''
                phone=''
                mailboxs=self.driver.find_elements(By.XPATH,'//*[contains(text(),"邮件")]/..')
                if len(mailboxs)!=0:
                    mailbox = '\n'.join(map(lambda e: e.text, mailboxs))
                else:
                    mailbox = ''
                introduces=self.driver.find_elements(By.XPATH,'//*[contains(text(),"个人")]/../following-sibling::*[1]')
                if len(introduces)!=0:
                    introduce = '\n'.join(map(lambda e: e.text, introduces))
                    introduce=introduce.strip()
                else:
                    introduce = ''
                typess=self.driver.find_elements(By.XPATH,'//*[@class="gp-f26"]')
                if len(typess)!=0:
                    types = '\n'.join(map(lambda e: e.text, typess))
                    types=types.strip()
                else:
                    types = ''
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
                self.driver.back()
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = ''
    #学校
    school='北京理工大学-医学技术学院'
    demo = LigongUniversityNo04(one_url,school)
    demo.start()
