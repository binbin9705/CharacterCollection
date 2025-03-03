import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNo16(object):
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
        # links = []
        # nums=self.driver.find_elements(By.XPATH,'//*[@class="sub_left"]/ul/li[1]//dl[@class="second_nav"]//a')
        # for n in nums:
        #     n=n.get_attribute("href")
        #     links.append(n)
        # print(links)
        # for link in links:
        counts=self.driver.find_elements(By.XPATH,'//*[@class="wrap_content"]//li')
        print(len(counts))
        for c in counts:
            low_url=self.driver.current_url
            name=c.find_element(By.XPATH,'.//div[@class="title fs20"]').text
            print(name)
            #进详情
            # self.driver.get(c.find_element(By.XPATH, './/a').get_attribute("href"))
            c.find_element(By.XPATH,'.//a').click()
            photos = self.driver.find_elements(By.XPATH, '//*[@class="wrap_content"]//img')
            if len(photos) != 0:
                photo = '\n'.join(map(lambda e: e.get_attribute("src"), photos))
            else:
                photo = ''
            introduces=self.driver.find_elements(By.XPATH,'//*[@class="wrap_content"]')
            if len(introduces)!=0:
                introduce = '\n'.join(map(lambda e: e.text, introduces))
                introduce=introduce.replace(' ', '')
            else:
                introduce = ''
            # print(introduce)
            p=self.driver.find_element(By.XPATH,'//*[@class="firstRow"]//descendant::span[text()[normalize-space()]][1]').text
            p = p.replace(' ', '')
            print(p)
            if p +'\n' in introduce:
                title = introduce.split( p +'\n')[1].split("\n")[0]
            else:
                title = ''
            if "研究方向\n" in introduce:
                field = introduce.split("研究方向\n")[1].split("\n")[0]
            else:
                field = ''
            if "办公电话：" in introduce:
                phone = introduce.split("办公电话：")[1].split("\n")[0]
            else:
                phone = ''
            if "电子邮件："in introduce:
                mailbox = introduce.split("电子邮件：")[1].split("\n")[0]
            else:
                mailbox = ''
            types=self.driver.find_element(By.XPATH,'//*[@class="sub_title_1 fs26"]').text
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
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url ='https://cst.bit.edu.cn/szdw/jsml/index.htm'
    #学校
    school='北京理工大学-网络空间安全学院'
    demo = LigongUniversityNo16(one_url,school)
    demo.start()
