import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class GJXY(object):
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
        # options.add_argument('--incognito')
        # 关掉浏览器记住密码弹窗
        prefs = {"": ""}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option("prefs", prefs)
        # options.headless=True
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
        count=self.driver.find_elements(By.XPATH,'//*[@id="wraper2"]/div[3]/ul//li//a[normalize-space()]')
        print(len(count))
        for x in count:
            link=x.get_attribute("href")
            # time.sleep(1)
            self.driver.get(link)
            print(link)
            # 姓名
            name = self.driver.find_element(By.XPATH,'//*[@id="wraper2"]/div[3]/div/h3').text
            name=name.split("(")[0]
            # print(name)
            #简介
            p_sss=self.driver.find_elements(By.XPATH,'.//div[@class="teacher_intr clearfix"]/following-sibling::*')
            topInfo='\n'.join(map(lambda e: e.text, p_sss))
            # 电子邮箱''
            p_s = self.driver.find_elements(By.XPATH, './/div[@class="teacher_intr clearfix"]//p')
            mailbox1 ='\n'.join(map(lambda e: e.text, p_s))
            mailbox=mailbox1.split("邮　箱：")[1]
            # print(mailbox)
            # 电话
            # phone =self.driver.find_element(By.XPATH,'//*[@id="wraper2"]/div[3]/div/div[1]/p[4]').text
            # phone=phone.split("：")[1]
            phone = mailbox1.split("电　话：")[1].split("邮　箱：")[0]
            # print(phone)
            #研究方向
            area=topInfo.split("研究方向")[1].split("讲授课程")[0]
            # print(area)
            #职称
            title=self.driver.find_element(By.XPATH,'//*[@id="wraper2"]/div[3]/div/div[1]/p[1]').text
            title=title.split("：")[1]
            # print(title)
            #荣誉称号
            area1=topInfo.split("社会兼职及荣誉")[1]
            # print(area1)
            # 照片
            photo = self.driver.find_element(By.XPATH,'//*[@id="wraper2"]/div[3]/div/div[1]/img').get_attribute("src")
            data = {}
            data['姓名'] = name
            data['研究领域'] = area
            data['职称'] = title
            data['荣誉称号'] = area1
            data['电话'] = phone
            data['邮箱'] = mailbox
            data['简介'] = topInfo
            data['照片'] = photo
            data['类型'] = '在岗教师'
            self.ResultList.append(data)
            print(data)
            time.sleep(1)
            self.driver.back()
            time.sleep(1)
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = 'http://ic.ruc.edu.cn/szdw/zgjs/index.htm'
    #学校
    school='人民大学-国际学院（苏州研究院）-国际学院'
    demo = GJXY(one_url,school)
    demo.start()
