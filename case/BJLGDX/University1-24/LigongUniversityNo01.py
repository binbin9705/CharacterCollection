import pandas as pd, time, logging, colorlog
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNo22(object):
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
        links=[]
        link=self.driver.find_elements(By.XPATH,'//*[@class="gp-second-nav"]//dd/a')
        for l in link:
            link=l.get_attribute("href")
            links.append(link)
        print(links)
        for link in links:
            self.driver.get(link)
            time.sleep(1)
            types=self.driver.find_element(By.XPATH,'//*[@class="gp-f22"]').text
            print(types)
            totals=self.driver.find_elements(By.XPATH,'//*[@class="notification"]//li//a')
            print(len(totals))
            tt=1
            for t in totals:
                time.sleep(1)
                times=self.driver.find_element(By.XPATH,'//*[@class="notification"]//li['+str(tt)+']//a//p').text
                print(times)
                self.driver.find_element(By.XPATH, '//*[@class="notification"]//li['+str(tt)+']//a//p').click()
                time.sleep(1)
                counts=self.driver.find_elements(By.XPATH,'//div[@class="teamBox"]//p[@class="teamname gp-f16"]')
                print(len(counts))
                tt+=1
                for c in counts:
                    low_url=self.driver.current_url
                    name=c.text
                    print(name)
                    photos = c.find_elements(By.XPATH, './../..//img')
                    if len(photos) != 0:
                        photo = '\n'.join(map(lambda e: e.get_attribute("src"), photos))
                    else:
                        photo = ''
                    # print(photo)
                    # 进详情
                    # c.click()
                    self.driver.get(c.find_element(By.XPATH,'./../..').get_attribute("href"))
                    time.sleep(0.5)
                    introduces=self.driver.find_elements(By.XPATH,'//*[@class="bandRight"]')
                    if len(introduces)!=0:
                        introduce = '\n'.join(map(lambda e: e.text, introduces))
                        introduce=introduce.replace(' ', '')
                    else:
                        introduce = ''
                     # print(introduce)
                    if "研究兴趣在" in introduce:
                        field = introduce.split("研究兴趣在")[1].split("。")[0]
                    elif"研究领域：" in introduce:
                        field = introduce.split("研究领域：")[1].split("\n")[0]
                    else:
                        field = ''
                    if "电话：" in introduce:
                        phone = introduce.split("电话：")[1].split("\n")[0]
                    else:
                        phone = ''
                    if "联系方式："in introduce:
                        mailbox = introduce.split("联系方式：")[1].split("\n")[0]
                    else:
                        mailbox = ''
                    title=''
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
                time.sleep(0.5)
                self.driver.back()
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx', encoding='xlsxwriter')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx',encoding='xlsxwriter')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    one_url ='https://qiushi.bit.edu.cn/szdw/dsdw/xsds/index.htm'
    #学校
    school='北京理工大学-求是书院'
    demo = LigongUniversityNo22(one_url,school)
    demo.start()
