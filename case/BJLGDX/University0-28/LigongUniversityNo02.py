import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNo02(object):
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
            'yxx/index.htm',
            'yxx/index1.htm',
            'swyxgcx/index.htm',
            'swyxgcx/index1.htm',
            'kjswyyxgcyjs/index.htm',
            'swsyjxzx/index.htm'
               ]
        for link in links:
            self.driver.get("https://ls.bit.edu.cn/szdw/qyjs/"+link)
            types=self.driver.find_element(By.XPATH,'//*[contains(text(),"当前位置")]/a').text
            print(link)
            if link=='swyxgcx/index.htm' or link=='kjswyyxgcyjs/index.htm':
                counts = self.driver.find_elements(By.XPATH, '//*[@class="box_list"]//li[1]/following-sibling::*')
            else:
                counts = self.driver.find_elements(By.XPATH, '//*[@class="box_list"]//li')
            print(len(counts))
            for c in counts:
                names=c.find_element(By.XPATH,'.//a').text
                print(names)
                if" —— " in names:
                    name1=names.split(" —— ")[1]
                elif" ——" in names:
                    name1=names.split(" ——")[1]
                elif"——" in names:
                    name1 = names.split("——")[1]
                else:
                    name1=names.split("--")[1]
                if " "in name1:
                    name=name1.split(" ")[0]
                    title=name1.split(" ")[1]
                    if "/"in title:
                        title=title.split("/")[0]
                else:
                    name=name1
                    title =''
                print(name)
                print(title)
                #进详情
                c.find_element(By.XPATH, './/a').click()
                #切title
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(1)
                introduces=self.driver.find_elements(By.XPATH,'//div[@class="wz_art"]')
                if len(introduces)!=0:
                    introduce='\n'.join(map(lambda e:e.text,introduces))
                    introduce=introduce.strip()
                    field = ''
                    honor = ''
                    phones = self.driver.find_elements(By.XPATH,'//*[contains(text(),"010-")]')
                    if len(phones)!=0:
                        phone='\n'.join(map(lambda e:e.text,phones))
                    else:
                        phone=''
                    mailboxs = self.driver.find_elements(By.XPATH,'//*[contains(text(),"@")]')
                    if len(mailboxs)!=0:
                        mailbox='\n'.join(map(lambda e:e.text,mailboxs))
                    else:
                        mailbox=''
                    photos =  self.driver.find_elements(By.XPATH,'//*[@class="box_list"]//img')
                    if len(photos)!=0:
                        photo='\n'.join(map(lambda e:e.get_attribute("src"),photos))
                    else:
                        photo=''
                else:
                    introduce=''
                    field=''
                    honor=''
                    phone=''
                    mailbox=''
                    photo=''
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
                print(data)
                self.ResultList.append(data)
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[-1])
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = 'https://ls.bit.edu.cn/szdw/qyjs/yxx/index.htm'
    #学校
    school='北京理工大学-生命学院'
    demo = LigongUniversityNo02(one_url,school)
    demo.start()
