import pandas as pd, time, logging, colorlog
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNo04(object):
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
        nuns=self.driver.find_elements(By.XPATH,'//*[@class="articleList03 articleList02"]')
        for n in nuns:
            types=n.find_element(By.XPATH,'.//h3').text
            print(types)
            counts=n.find_elements(By.XPATH,'.//li')
            print(len(counts))
            for c in counts:
                low_url=self.driver.current_url
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
                if "研究方向\n" in introduce and "团队介绍" in introduce:
                    field = introduce.split("研究方向\n")[1].split("团队介绍")[0]
                elif"研究方向\n" in introduce and "\n论文" in introduce:
                    field = introduce.split("研究方向\n")[1].split("\n论文")[0]
                elif "研究方向\n" in introduce and "。\n" in introduce:
                    field = introduce.split("研究方向\n")[1].split("。\n")[0]
                elif"研究方向\n" in introduce:
                    field = introduce.split("研究方向\n")[1].split("\n")[0]
                elif"研究方向：\n" in introduce and "\n联系方式：" in introduce:
                    field = introduce.split("研究方向：\n")[1].split("\n联系方式：")[0]
                else:
                    field = ''
                if name+"，" in introduce:
                    title=introduce.split(name+"，")[1].split("，")[0]
                else:
                    title=''
                if "电话：" in introduce:
                    phone = introduce.split("电话：")[1].split("\n")[0]
                else:
                    phone = ''
                if "邮箱："in introduce:
                    mailbox = introduce.split("邮箱：")[1].split("\n")[0]
                elif "Email：" in introduce:
                    mailbox = introduce.split("Email：")[1].split("\n")[0]
                elif "电子邮件：" in introduce:
                    mailbox = introduce.split("电子邮件：")[1].split("\n")[0]
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
    one_url ='https://sme.bit.edu.cn/gbszdw/gbjxzy/index.htm'
    #学校
    school='北京理工大学-经管书院'
    demo = LigongUniversityNo04(one_url,school)
    demo.start()
