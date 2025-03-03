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
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
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
            'szml/index.htm',
            'dsfc/index.htm',
            'jcrc20/index.htm',
            'jxms/index.htm'
               ]
        for link in links[0:]:
            self.driver.get("https://sae.bit.edu.cn/szdw20/"+link)
            types=self.driver.find_element(By.XPATH,'//a[@class="active"]').text
            counts=self.driver.find_elements(By.XPATH,'//div[@class="mulList"]//li')
            if len(counts)==0:
                counts=self.driver.find_elements(By.XPATH,'//div[@class="subList02 ul-inline"]//li')
            print(len(counts))
            for c in counts:
                c.find_element(By.XPATH,'.//a').click()
                names=self.driver.find_elements(By.XPATH,'//*[contains(@class,"f24")]')
                if len(names) != 0:
                    name = '\n'.join(map(lambda e: e.text, names))
                elif len(self.driver.find_elements(By.XPATH,'//div[@class="articleTitle02"]//h2'))!=0:
                    name = '\n'.join(map(lambda e: e.text, self.driver.find_elements(By.XPATH,'//div[@class="articleTitle02"]//h2')))
                else:
                    name = ''
                print(name)
                phones=self.driver.find_elements(By.XPATH,'//*[contains(text(),"电话")]')
                if len(phones)!=0:
                    phone = '\n'.join(map(lambda e: e.text, phones))
                else:
                    phone=''
                titels=self.driver.find_elements(By.XPATH,'//*[contains(text(),"职 称")]')
                if len(titels)!=0:
                    title = '\n'.join(map(lambda e: e.text, titels))
                else:
                    title=''
                mailboxs=self.driver.find_elements(By.XPATH,'//*[contains(text(),"邮 箱")]')
                if len(mailboxs)!=0:
                    mailbox = '\n'.join(map(lambda e: e.text, mailboxs))
                else:
                    mailbox=''
                fields=self.driver.find_elements(By.XPATH,'//*[contains(text(),"研究领域")]//following-sibling::*[1]')
                if len(fields)!=0:
                    field = '\n'.join(map(lambda e: e.text, fields))
                else:
                    field=''
                if len(self.driver.find_elements(By.XPATH,"//*[@class='teacherBottom']"))!=0:
                    introduce='\n'.join(map(lambda e:e.text,self.driver.find_elements(By.XPATH,"//*[@class='teacherBottom']")))
                    introduce=introduce.strip()
                    'class="article02"'
                elif len(self.driver.find_elements(By.XPATH,"//*[@class='article gp-f16']"))!=0:
                    introduce = '\n'.join(map(lambda e: e.text, self.driver.find_elements(By.XPATH,"//*[@class='article gp-f16']")))
                    introduce = introduce.strip()
                elif len(self.driver.find_elements(By.XPATH,'//*[@class="article02"]'))!=0:
                    introduce = '\n'.join(map(lambda e: e.text, self.driver.find_elements(By.XPATH,'//*[@class="article02"]')))
                    introduce = introduce.strip()
                else:
                    introduce=''
                photos=self.driver.find_elements(By.XPATH,'//*[contains(@class,"f24")]/../..//img')
                if len(photos)!=0:
                    photo = '\n'.join(map(lambda e: e.get_attribute("src"), photos))
                elif len(self.driver.find_elements(By.XPATH,'//*[@class="article02"]//img'))!=0:
                    photo = '\n'.join(map(lambda e: e.get_attribute("src"), self.driver.find_elements(By.XPATH,'//*[@class="article02"]//img')))
                else:
                    photo=''
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
    one_url = 'https://sae.bit.edu.cn/szdw20/szml/index.htm'
    #学校
    school='北京理工大学-宇航学院'
    demo = LigongUniversityNO01(one_url,school)
    demo.start()
