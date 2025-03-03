import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNo20(object):
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
        links = []
        nums=self.driver.find_elements(By.XPATH,'//*[@id="gp-subLeft"]//a')
        for n in nums:
            # print(n.text)
            n_link=n.get_attribute("href")
            links.append(n_link)
        # print(links)
        for link in links:
            self.driver.get(link)
            counts=self.driver.find_elements(By.XPATH,'//*[@class="gp-teacher5"]/ul//a')
            print(len(counts))
            for c in counts:
                low_url=self.driver.current_url
                name=c.find_element(By.XPATH,'.//div[text()[normalize-space()]]').text
                if "讲师" in name:
                    name = name.split("讲师")[0]
                    title = '讲师'
                elif "助理教授" in name:
                    name = name.split("助理教授")[0]
                    title = '助理教授'
                elif "副教授" in name:
                    name = name.split("副教授")[0]
                    title = '副教授'
                else:
                    name = name.split("教授")[0]
                    title = '教授'
                print(name)
                photos = c.find_elements(By.XPATH, './/img')
                if len(photos) != 0:
                    photo = '\n'.join(map(lambda e: e.get_attribute("src"), photos))
                else:
                    photo = ''
                # 进详情
                # c.click()
                self.driver.get(c.get_attribute("href"))
                types = self.driver.find_element(By.XPATH, '//*[@class="gp-bread gpTextArea "]//a[3]').text
                introduces=self.driver.find_elements(By.XPATH,'//*[@class="gp-article1 gp-article gp-f16"]')
                if len(introduces)!=0:
                    introduce = '\n'.join(map(lambda e: e.text, introduces))
                    introduce=introduce.replace(' ', '')
                else:
                    introduce = ''
                 # print(introduce)
                if "研究方向为" in introduce:
                    field = introduce.split("研究方向为")[1].split("。")[0]
                elif "研究方向" in introduce:
                    field = introduce.split("研究方向")[1].split("\n")[0]
                elif "研究领域和方向\n" in introduce:
                    field=introduce.split("研究领域和方向\n")[1].split("\n\n")[0]
                elif "研究专长：" in introduce and "代表性成果" in introduce:
                    field = introduce.split("研究专长：")[1].split("代表性成果")[0]
                elif "究兴趣包括" in introduce:
                    field = introduce.split("究兴趣包括")[1].split("。")[0]
                elif "科研方向\n" in introduce:
                    field = introduce.split("科研方向\n")[1].split("代表性学术成果")[0]
                elif "研究方向:" in introduce:
                    field = introduce.split("研究方向:")[1].split("\n")[0]
                else:
                    field = ''
                if "电话：" in introduce:
                    phone = introduce.split("电话：")[1].split("\n")[0]
                else:
                    phone = ''
                if "邮件："in introduce:
                    mailbox = introduce.split("邮件：")[1].split("\n")[0]
                elif "E-mail：" in introduce:
                    mailbox = introduce.split("E-mail：")[1].split("\n")[0]
                elif "邮箱：" in introduce:
                    mailbox=introduce.split("邮箱：")[1].split("\n")[0]
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
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    one_url ='https://sfl.bit.edu.cn/szdw/xsjrc/index.htm'
    #学校
    school='北京理工大学-外国语学院'
    demo = LigongUniversityNo20(one_url,school)
    demo.start()
