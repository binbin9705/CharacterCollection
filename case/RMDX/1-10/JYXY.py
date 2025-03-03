import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class GJGXXY(object):
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
        # 在职教师
        self.driver.get(self.one_url)
        counts=self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div/ul//a')
        print(len(counts))
        for x in counts:
            x.click()
            # 姓名
            name = self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div[2]/form/div/div[1]/div[2]/p').text
            name = name.split("，")[0]
            #研究领域
            study=self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div[2]/form/div/div[1]/div[2]/span').text
            #简介
            ps=self.driver.find_elements(By.XPATH,'//*[@id="vsb_content"]/div//div')
            topInfo='\n'.join(map(lambda e: e.text, ps))
            # 电话
            psss=self.driver.find_elements(By.XPATH,'//*[@id="vsb_content"]/div//p[contains(text(),"电话：")]')
            phone = '\n'.join(map(lambda e: e.text, psss))
            if str(phone) != "":
                phone = phone.split("电话：")[1]
            print(phone)
            # 电子邮箱
            pss=self.driver.find_elements(By.XPATH,'//*[@id="vsb_content"]/div//p[contains(text(),"邮箱：")]')
            mailbox = '\n'.join(map(lambda e: e.text, pss))
            if str(mailbox)!="":
                mailbox=mailbox.split("邮箱：")[1]
            # 照片
            photo= self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div[2]/form/div/div[1]/div[1]').get_attribute("style")
            photo=photo.split('url("')[1].split('")')[0]
            photo="http://soe.ruc.edu.cn"+photo
            data = {}
            data['姓名'] = name
            data['研究领域'] = study
            data['职称'] = '教授'
            data['荣誉称号'] = topInfo
            data['电话'] = phone
            data['邮箱'] = mailbox
            data['简介'] = topInfo
            data['照片'] = photo
            data['类型'] = types
            self.ResultList.append(data)
            print(data)
            self.driver.back()
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = 'http://soe.ruc.edu.cn/szdw/zzjs.htm'
    types = '在职教师'
    #学校
    school='人民大学-教育学院'
    demo = GJGXXY(one_url,school)
    demo.start()

