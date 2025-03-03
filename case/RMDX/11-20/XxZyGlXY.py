import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class XxZyGlXY(object):
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
        counts=self.driver.find_elements(By.XPATH,'//*[@id="teacher"]/div[2]/ul//li')
        print(len(counts))
        x=1
        for c in counts:
            # print(c)
            #姓名
            # name=c.find_element(By.XPATH,'.//h3').text
            name=self.driver.find_element(By.XPATH,'//*[@id="teacher"]/div[2]/ul/li['+str(x)+']//h3').text
            print(name)
            #照片
            # photo=c.find_element(By.XPATH,'.//img').get_attribute("src")
            photo=self.driver.find_element(By.XPATH,'//*[@id="teacher"]/div[2]/ul/li['+str(x)+']//img').get_attribute("src")
            #职称
            # title=c.find_element(By.XPATH,'.//p').text
            title=self.driver.find_element(By.XPATH,'//*[@id="teacher"]/div[2]/ul/li['+str(x)+']//p').text
            #研究领域
            # field=c.find_element(By.XPATH,'.//div[@class="subject"]').text
            field=self.driver.find_element(By.XPATH,'//*[@id="teacher"]/div[2]/ul/li['+str(x)+']//div[@class="subject"]').text
            field=field.split("研究方向：")[1]
            #人物详情
            # links=c.find_element(By.XPATH,'./a').get_attribute('href')
            links=self.driver.find_element(By.XPATH,'//*[@id="teacher"]/div[2]/ul/li['+str(x)+']/a').get_attribute('href')
            self.driver.get(links)
            #电话
            phones=self.driver.find_elements(By.XPATH,'//li[contains(text(),"电话")]')
            if len(phones)!=0:
                phone = '\n'.join(map(lambda e: e.text, phones))
            else:
                phone=''
            #邮箱
            mailboxs = self.driver.find_elements(By.XPATH, '//li[contains(text(),"邮箱")]')
            if len(mailboxs)!=0:
                mailbox = '\n'.join(map(lambda e: e.text, mailboxs))
            else:
                mailbox=''
            #荣誉称号
            honor=''
            # 简介
            introduce = self.driver.find_elements(By.XPATH, '//div[contains(text(),"个人简历")]/..')
            introduce='\n'.join(map(lambda e:e.text,introduce))
            # print(introduce)
            data = {}
            data['姓名'] = name
            data['研究领域'] = field
            data['职称'] = title
            data['荣誉称号'] = honor
            data['电话'] = phone
            data['邮箱'] = mailbox
            data['简介'] = introduce
            data['照片'] = photo
            data['类型'] =types
            self.ResultList.append(data)
            print(data)
            self.driver.back()
            x+=1

        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    # 在职教师
    one_url = 'https://irm.ruc.edu.cn/szdw/zzjs/ajysfl/z_qb/index.htm'
    types='在职教师'
    # 学校
    school = '人民大学-信息资源管理学院'
    demo = XxZyGlXY(one_url, school)
    demo.start()
