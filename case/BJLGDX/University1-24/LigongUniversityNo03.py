import pandas as pd, time, logging, colorlog
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNo03(object):
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
        links=[
            'https://xjjg.bit.edu.cn/yjtd/zrjs/index.htm',
            'https://xjjg.bit.edu.cn/yjtd/zrjs/index1.htm',
            'https://xjjg.bit.edu.cn/yjtd/zrjs/index2.htm'
        ]
        for link in links:
            self.driver.get(link)
            time.sleep(0.5)
            types='研究团队'
            counts=self.driver.find_elements(By.XPATH,'//*[@class="pictureList pictureList2"]//li')
            print(len(counts))
            for c in counts:
                low_url=self.driver.current_url
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
                name = self.driver.find_element(By.XPATH, '//*[@class="articleTitle"]//h2').text
                names = name.replace(' ', '')
                if "党委书记" in names:
                    name = names.split("党委书记")[0]
                    title = names.split(name)[1]
                elif "副院长" in names:
                    name = names.split("副院长")[0]
                    title = names.split(name)[1]
                elif "院长助理" in names:
                    name = names.split("院长助理")[0]
                    title = names.split(name)[1]
                elif "院士" in names:
                    name = names.split("院士")[0]
                    title = names.split(name)[1]
                elif "副教授" in names:
                    name = names.split("副教授")[0]
                    title = names.split(name)[1]
                elif "研究员" in names:
                    name = names.split("研究员")[0]
                    title = names.split(name)[1]
                elif "助理" in names:
                    name = names.split("助理")[0]
                    title = names.split(name)[1]
                elif "博士后" in names:
                    name = names.split("博士后")[0]
                    title = names.split(name)[1]
                else:
                    name = names.split("教授")[0]
                    title = names.split(name)[1]
                print(name)
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
                if "电话：" in introduce:
                    phone = introduce.split("电话：")[1].split("邮箱")[0]
                else:
                    phone = ''
                if "邮箱："in introduce:
                    mailbox = introduce.split("邮箱：")[1].split("\n")[0]
                elif "联系方式：\n" in introduce:
                    mailbox = introduce.split("联系方式：\n")[1].split("\n")[0]
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
            df.to_excel('./人才-' + self.school + '.xlsx', encoding='xlsxwriter')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx',encoding='xlsxwriter')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    one_url ='https://arims.bit.edu.cn/xztd/jsml/fzhjkxtcyjs/index.htm'
    #学校
    school='北京理工大学-先进结构技术研究院'
    demo = LigongUniversityNo03(one_url,school)
    demo.start()
