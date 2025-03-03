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
        count=self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div/div[2]/div/div[2]/table/tbody/tr[*]/td[2]/a')
        print(len(count))
        for x in count:
            link=x.get_attribute("href")
            self.driver.get(link)
            print(link)
            # 姓名
            name = self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div[2]/div/div[1]/div[2]/span[1]').text
            # print(name)
            #简介
            topInfo1=self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div[2]/div/div[1]/div[2]/p').text
            topInfo2=self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div/div[2]/div/div[2]/div')
            topInfo3 = '\n'.join(map(lambda e: e.text, topInfo2))
            topInfo=topInfo1+'\n'+topInfo3
            # 电子邮箱''
            if str(topInfo).find("Email")!=-1 and str(topInfo).find("个人简介")!=-1:
                mailbox = topInfo.split("Email")[1].split("个人简介")[0]
            else:
                mailbox =''
            # 电话
            phone =''
            #研究领域
            if str(topInfo).find("主要研究方向为")!=-1 and str(topInfo).find("主要学术兼职")!=-1:
                area = topInfo.split("主要研究方向为")[1].split("主要学术兼职")[0]
            else:
                area =''
            #职称
            if str(topInfo).find("职称")!=-1 and str(topInfo).find("个人简介")!=-1 and str(topInfo).find("Email")!=-1 :
                title = topInfo.split("职称")[1].split("Email")[0]
            elif str(topInfo).find("职称")!=-1 and str(topInfo).find("个人简介")!=-1:
                title = topInfo.split("职称")[1].split("个人简介")[0]
            else:
                title =''
            #荣誉称号
            area1=topInfo
            # 照片
            photo = self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div[2]/div/div[1]/div[1]/img').get_attribute("src")
            data = {}
            data['姓名'] = name
            data['研究领域'] = area
            data['职称'] = title
            data['荣誉称号'] = area1
            data['电话'] = phone
            data['邮箱'] = mailbox
            data['简介'] = topInfo
            data['照片'] = photo
            data['类型'] = '师资团队'
            self.ResultList.append(data)
            print(data)
            time.sleep(1)
            self.driver.back()
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = 'http://srs.ruc.edu.cn/szdw/index.htm'
    #学校
    school='人民大学-国际学院（苏州研究院）-丝路学院'
    demo = GJXY(one_url,school)
    demo.start()
