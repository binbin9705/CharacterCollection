import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class JJXY(object):
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
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 不显示chrome受自动控制提示
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
        # self.driver.find_element(By.XPATH,'/html/body/section/div/div[3]/div[2]/div[2]/ul/li[5]/a').click()
        time.sleep(3)
        element=self.driver.find_elements(By.XPATH,'/html/body/section/div/div[3]/div[2]/div[2]/ul/li')
        # element=['C','D','F','G','H','J','K','L','M','N','P','Q','S','T','W','X','Y','Z']
        for x in element[1:]:
            x1 = x.text
            print(x1)
            if x1!="C":
                x.click()
            count=self.driver.find_elements(By.XPATH,'/html/body/section/div/div[3]/div[2]/ul[2]/li')
            print(len(count))
            for c in count:
                # c.find_element(By.XPATH,'.//a[@class="more"]').click()
                c.find_element(By.XPATH,'.//a').click()
                # 姓名
                name = self.driver.find_element(By.XPATH,'/html/body/section/div/div[3]/div[1]/div').text
                # 职称
                title = self.driver.find_element(By.XPATH,'/html/body/section/div/div[3]/div[1]/ul/li[2]').text
                # 电子邮箱
                mailbox = self.driver.find_element(By.XPATH,'/html/body/section/div/div[3]/div[1]/ul/li[5]').text
                # 电话
                phone = self.driver.find_element(By.XPATH,'/html/body/section/div/div[3]/div[1]/ul/li[3]').text
                #研究领域
                areas1=self.driver.find_element(By.XPATH,'/html/body/section/div/div[3]/div[1]/ul/li[6]').text
                #荣誉称号
                p_s = self.driver.find_elements(By.XPATH, './/div[@class="teacherDetail"]/div[not(@class="teacherInfo")]')
                area = '\n'.join(map(lambda e: e.text, p_s))
                # 照片
                photo = self.driver.find_element(By.XPATH,'/html/body/section/div/div[2]/div[1]/img').get_attribute("src")
                data = {}
                data['姓名'] = name
                data['研究领域'] = areas1
                data['职称'] = title
                data['荣誉称号'] = area
                data['电话'] = phone
                data['邮箱'] = mailbox
                data['简介'] = area
                data['照片'] = photo
                data['类型'] = title
                self.ResultList.append(data)
                print(data)
                self.driver.back()
            if x1!= "C":
                self.driver.back()
                time.sleep(1)
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    # one_url = 'http://econ.ruc.edu.cn/szdw/jsml/apypx/C/index.htm'
    one_url = 'http://econ.ruc.edu.cn/szdw/jsml/apypx/C/index.htm'
    #学校
    school='人民大学-经济学院'
    demo = JJXY(one_url,school)
    demo.start()
