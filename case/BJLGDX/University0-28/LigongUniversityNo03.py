import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNo03(object):
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
        '''
        缪林清人员数据有问题 跳开爬
        :return:
        '''
        self.driver = webdriver.Chrome(options=self.options())
        self.driver.get(self.one_url)
        counts=self.driver.find_elements(By.XPATH,'//*[@class="box_list"]//li')
        print(len(counts))
        for c in counts[186:]:
            c.find_element(By.XPATH,'.//a').click()
            # time.sleep(0.5)
            lists=self.driver.find_element(By.XPATH,'//*[contains(text(),"姓名")]/..').text
            if "姓名：" in lists:
                name=lists.split("姓名：")[1].split("\n")[0]
            else:
                name=''
            if"研究方向：" in lists:
                field = lists.split("研究方向：")[1].split("\n")[0]
            else:
                field=''
            if "职称："in lists:
                title = lists.split("职称：")[1].split("\n")[0]
            else:
                title=''
            if "联系电话："in lists:
                phone = lists.split("联系电话：")[1].split("\n")[0]
            else:
                phone=''
            if "E-mail："in lists:
                mailbox = lists.split("E-mail：")[1].split("\n")[0]
            else:
                mailbox=''
            photo=self.driver.find_element(By.XPATH,'//*[@class="artic2"]//img').get_attribute("src")

            typess=self.driver.find_element(By.XPATH,'//*[@class="paget_add"]').text
            if " 师资名单» "in typess:
                types = typess.split("师资名单» ")[1]
                types=types.strip()

            else:
                types=''
            introduces=self.driver.find_elements(By.XPATH,'//*[@class="con_teacher"]')
            if len(introduces)!=0:
                introduce='\n'.join(map(lambda e:e.text,introduces))
            else:
                introduce=''
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
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = 'https://smen.bit.edu.cn/sztd/szms/index.htm'
    #学校
    school='北京理工大学-机电学院'
    demo = LigongUniversityNo03(one_url,school)
    demo.start()
