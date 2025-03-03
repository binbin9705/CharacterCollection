import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class HJXY(object):
    def __init__(self, one_url, school):
        self.one_url = one_url
        self.school = school
        # 表头
        self.title = ['姓名', '研究领域', '职称', '荣誉称号', '电话', '邮箱', '简介', '照片', '类型']
        self.ResultList = []  # 最终数据

    def options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")  # 规避监测selenium
        options.add_argument('--start-maximized')  # 全屏运行
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 不显示chrome受自动控制提示
        # 关掉浏览器记住密码弹窗
        prefs = {"": ""}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option("prefs", prefs)
        return options

    def isElementPresent(self, by, value):
        try:
            element = self.driver.find_element(by=by, value=value)
        except NoSuchElementException as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True

    def start(self):
        self.driver = webdriver.Chrome(options=self.options())
        self.driver.get(self.one_url)
        # 全职教师
        counts=self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/ul/li')
        for z in counts:
            print(z.find_element(By.XPATH,'.//a').get_attribute('href'))
            #照片
            photo=z.find_element(By.XPATH, './/img').get_attribute('src')
            # print(photo)
            #姓名
            names=z.find_element(By.XPATH,'.//h3').text
            name=names.split(" ")[0]
            title=names.split(" ")[1]
            # print(name)
            # print(title)
            #研究领域
            fields=z.find_elements(By.XPATH,'.//p[contains(text(),"研究领域：")]')
            if len(fields) != 0:
                fields = '\n'.join(map(lambda e: e.text, fields))
                field=fields.split("研究领域：")[1]
            else:
                field=''
            # print(field)
            #进人物详情
            self.driver.get(z.find_element(By.XPATH, './/a').get_attribute('href'))
            #邮箱
            mailboxs = self.driver.find_elements(By.XPATH, '//p[contains(text(),"电子邮件：")]')
            if len(mailboxs)!=0:
                mailboxs = '\n'.join(map(lambda e: e.text, mailboxs))
                mailbox=mailboxs.split("电子邮件：")[1]
            else:
                mailbox=""
            #联系方式
            phones = self.driver.find_elements(By.XPATH, '//p[contains(text(),"联系电话：")]')
            if len(phones) != 0:
                phones = '\n'.join(map(lambda e: e.text, phones))
                phone = phones.split("联系电话：")[1]
            else:
                phone = ""
            #简介
            introduce=''
            introduces=self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/nav/ul//li')
            # print(len(introduces))
            for x in introduces:
                x.click()
                introduce1 = self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/div[1]/div[not(@style) or @style="display: block;"]')
                introduce1 = '\n'.join(map(lambda e: e.text, introduce1))
                introduce+='\n'+introduce1

            #奖励荣誉
            honor=''
            honor1 = self.driver.find_elements(By.XPATH, '//li[contains(text(),"奖励荣誉")]')
            if len(honor1)!=0:
                self.driver.find_element(By.XPATH, '//li[contains(text(),"奖励荣誉")]').click()
                honors = self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/div[1]/div[not(@style) or @style="display: block;"]')
                honor='\n'.join(map(lambda e:e.text,honors))
                honor+='\n'+honor
            data = {}
            data['姓名'] = name
            data['研究领域'] = field
            data['职称'] = title
            data['荣誉称号'] = honor
            data['电话'] = phone
            data['邮箱'] = mailbox
            data['简介'] = introduce
            data['照片'] = photo
            data['类型'] ='全职教师'
            self.ResultList.append(data)
            print(data)
            self.driver.back()
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    # 在职教师
    one_url = 'https://envi.ruc.edu.cn/szdw/qzjs/xb/qb_qz/index.htm'
    # 学校
    school = '人民大学-环境学院'
    demo = HJXY(one_url, school)
    demo.start()
