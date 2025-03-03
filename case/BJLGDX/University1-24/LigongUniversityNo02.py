import pandas as pd, time, logging, colorlog
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNo02(object):
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
        link=self.driver.find_elements(By.XPATH,'//*[@class="bit-list12 bit-list122 gp-ul-inline"]//li//a')
        for l in link:
            link=l.get_attribute("href")
            links.append(link)
        print(links)
        for link in links:
            self.driver.get(link)
            time.sleep(0.5)
            types=self.driver.find_elements(By.XPATH,'//*[@class="gp-bread"]')
            types = '\n'.join(map(lambda e: e.text, types))
            types=types.split("教师名录-")[1]
            print(types)
            counts=self.driver.find_elements(By.XPATH,'//*[@class="bit-list13 gp-avg-md-5 gp-avg-sm-3 gp-avg-xxs-2"]//li')
            print(len(counts))
            for c in counts:
                low_url=self.driver.current_url
                name=c.find_element(By.XPATH,'.//strong').text
                print(name)
                photos = c.find_elements(By.XPATH, './/img')
                if len(photos) != 0:
                    photo = '\n'.join(map(lambda e: e.get_attribute("src"), photos))
                else:
                    photo = ''
                # print(photo)
                # 进详情
                # c.click()
                self.driver.get(c.find_element(By.XPATH,'.//a').get_attribute("href"))
                time.sleep(0.5)
                introduces=self.driver.find_elements(By.XPATH,'//*[@class="gp-container wzMode1 pd4568"]//div[@class="teacherCon" or @class="teacherList"]')
                if len(introduces)!=0:
                    introduce = '\n'.join(map(lambda e: e.text, introduces))
                    introduce=introduce.replace(' ', '')
                else:
                    introduce = ''
                 # print(introduce)
                if "研究方向\n" in introduce and "团队介绍" in introduce:
                    field = introduce.split("研究方向\n")[1].split("团队介绍")[0]
                elif"研究方向\n" in introduce and "\n论文" in introduce:
                    field = introduce.split("研究方向\n")[1].split("\n论文")[0]
                elif "研究方向\n" in introduce and "。\n" in introduce:
                    field = introduce.split("研究方向\n")[1].split("。\n")[0]
                elif"研究方向\n" in introduce:
                    field = introduce.split("研究方向\n")[1].split("\n")[0]
                else:
                    field = ''
                if "联系电话：" in introduce:
                    phone = introduce.split("联系电话：")[1].split("E-mail")[0]
                else:
                    phone = ''
                if "E-mail："in introduce:
                    mailbox = introduce.split("E-mail：")[1].split("办公室地点")[0]
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
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx', encoding='xlsxwriter')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx',encoding='xlsxwriter')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    one_url ='https://arims.bit.edu.cn/xztd/jsml/fzhjkxtcyjs/index.htm'
    #学校
    school='北京理工大学-前沿交叉科学研究院'
    demo = LigongUniversityNo02(one_url,school)
    demo.start()
