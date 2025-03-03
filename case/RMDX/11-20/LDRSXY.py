import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LDRSXY(object):
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
        #先循环有多少人
        # counts = self.driver.find_elements(By.XPATH, '/html/body/div/div[3]/div[1]/div[2]/ul//li')
        # for c in counts:
        #     #获取文本是否是预期值
        #     nums2=self.driver.find_element(By.XPATH,'/html/body/div/div[3]/div[1]/div[2]/div[3]/span').text
        #     if "当前第 4 页"in nums2:
        #         continue
        #     else:
        #         #不是预期值翻页
        #         self.driver.find_element(By.XPATH, '/html/body/div/div[3]/div[1]/div[2]/div[3]/div/a[6]').click()

        #另外一思路
        # counts = self.driver.find_elements(By.XPATH, '/html/body/div/div[3]/div[1]/div[2]/ul//li')
        # for c in counts:
        #     #判断是否翻到第四页
        #     nums1=self.driver.find_elements(By.XPATH,'//a[text()="4" and @style="background-color:#ae0a29; color:#ffffff;" ]')
        # #     if len(nums1)!=1:
        #         #如果没翻到翻页
        #         self.driver.find_element(By.XPATH,'/html/body/div/div[3]/div[1]/div[2]/div[3]/div/a[6]').click()
        # #         print("翻了")


        #又另一套
        nums=['index.htm','index1.htm','index2.htm','index3.htm']
        for n in nums:
            link='http://slhr.ruc.edu.cn/szdw/zzjs/qb/'+n+''
            print(link)
            self.driver.get(link)
            counts=self.driver.find_elements(By.XPATH,'/html/body/div/div[3]/div[1]/div[2]/ul//li')
            for c in counts:
                #姓名
                name=c.find_element(By.XPATH,'.//span[1]').text
                name=name.split("姓名：")[1]
                #照片
                photo=c.find_element(By.XPATH,'.//img').get_attribute("src")
                #职称
                title=c.find_element(By.XPATH,'.//span[2]').text
                #电话
                phone=c.find_element(By.XPATH,'.//span[4]').text
                #邮箱
                mailbox = c.find_element(By.XPATH, './/span[5]').text
                links=c.find_element(By.XPATH,'.//a').get_attribute('href')
                self.driver.get(links)
                # 研究领域
                field = self.driver.find_elements(By.XPATH, '/html/body/div/div[3]/div[1]/div[2]/div[3]/div[1]')
                field = '\n'.join(map(lambda e: e.text, field))
                #荣誉称号
                honor=''
                # 简介
                introduce = self.driver.find_elements(By.XPATH, '/html/body/div/div[3]/div[1]/div[2]/div[starts-with(@class,"resume")]/*')
                introduce='\n'.join(map(lambda e:e.text,introduce))
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
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')

        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    # 在职教师
    one_url = 'http://slhr.ruc.edu.cn/szdw/zzjs/qb/index.htm'
    types='全职教师'
    # 学校
    school = '人民大学-劳动人事学院'
    demo = LDRSXY(one_url, school)
    demo.start()
