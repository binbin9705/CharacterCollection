import pandas as pd, time, logging, colorlog
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNo21(object):
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
        '''
        第二页第4个人信息有问题 分开取
        :return:
        '''
        self.driver = webdriver.Chrome(options=self.options())
        links = [
            'https://cce.bit.edu.cn/szdw/jsml/index.htm',
            'https://cce.bit.edu.cn/szdw/jsml/index1.htm',
            'https://cce.bit.edu.cn/szdw/jsml/index2.htm',
            'https://cce.bit.edu.cn/szdw/jsml/index3.htm',
            'https://cce.bit.edu.cn/szdw/jsml/index4.htm',
            'https://cce.bit.edu.cn/szdw/jsml/index5.htm',
            'https://cce.bit.edu.cn/szdw/jsml/index6.htm',
            'https://cce.bit.edu.cn/szdw/jsml/index7.htm'
        ]
        for link in links[3:]:
            self.driver.get(link)
            counts=self.driver.find_elements(By.XPATH,'//div[@class="apparPic gp-img-responsive"]')
            print(len(counts))
            for c in counts:
                low_url=self.driver.current_url
                names=c.find_element(By.XPATH,'.//following-sibling::div[1]').text
                print(names)
                if "\n" in names:
                    name = names.split("\n")[0]
                    title =names.split("\n")[1]
                elif "\n" not in names:
                    name=names
                    title=''
                else:
                    name=names
                    title=''
                print(name)
                photos = c.find_elements(By.XPATH, './/img')
                if len(photos) != 0:
                    photo = '\n'.join(map(lambda e: e.get_attribute("src"), photos))
                else:
                    photo = ''
                # print(photo)
                # 进详情
                time.sleep(0.5)
                c.click()
                time.sleep(0.5)
                # self.driver.get(c.get_attribute("href"))
                introduces=self.driver.find_elements(By.XPATH,'//*[@class="detailRight"]')
                if len(introduces)!=0:
                    introduce = '\n'.join(map(lambda e: e.text, introduces))
                    introduce=introduce.replace(' ', '')
                else:
                    introduce = ''
                 # print(introduce)
                if "研究领域和方向\n" in introduce:
                    field = introduce.split("研究领域和方向\n")[1].split("教育背景")[0]
                else:
                    field = ''
                if "电话：" in introduce:
                    phone = introduce.split("电话：")[1].split("\n")[0]
                else:
                    phone = ''
                if "电子邮箱："in introduce:
                    mailbox = introduce.split("电子邮箱：")[1].split("\n")[0]
                elif "E-mail：" in introduce:
                    mailbox = introduce.split("E-mail：")[1].split("\n")[0]
                else:
                    mailbox = ''
                types = '教师名录'
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
            df.to_excel('./人才-' + self.school + '.xlsx',encoding='xlsxwriter')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx',encoding='xlsxwriter')
        # self.driver.quit()
        print("完成")

if __name__ == '__main__':
    one_url ='https://cce.bit.edu.cn/szdw/jsml/index.htm'
    #学校
    school='北京理工大学-化学与化工学院'
    demo = LigongUniversityNo21(one_url,school)
    demo.start()
