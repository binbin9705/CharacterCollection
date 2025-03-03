import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class RenminUniversityNo53(object):
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

    def start(self):
        self.driver = webdriver.Chrome(options=self.options())
        self.driver.get(self.one_url)
        #查组织多少
        #循环进每个组织-判断有多少人-循环
        #拿每个组织的人才信息
        li=self.driver.find_elements(By.XPATH,'//ul[@id="SubMenu"]//li')
        ll=1
        for l in li:
            #l第一次在管理团队 第二次在研究团队
            types = l.find_element(By.XPATH, './a').text
            if ll!=1:
                l.find_element(By.XPATH,'./a').click()
            counts=self.driver.find_elements(By.XPATH,'//ul[@class="subPictrueList"]//li')
            for c in counts:
                name=c.find_element(By.XPATH,'.//p').text
                print(name)
                photo=c.find_element(By.XPATH,'.//img').get_attribute('src')
                c.find_element(By.XPATH, './/p').click()
                field=''
                title=''
                honor=''
                mailbox=''
                phone=''
                introduces=self.driver.find_elements(By.XPATH,'//div[@class="article"]')
                if len(introduces)!=0:
                    introduce='\n'.join(map(lambda e:e.text,introduces))
                else:
                    introduce=''
                data={}
                data['姓名']=name
                data['研究领域'] = field
                data['职称'] = title
                data['荣誉称号'] = honor
                data['电话'] = phone
                data['邮箱'] = mailbox
                data['简介'] = introduce
                data['照片'] = photo
                data['类型'] = types
                print(data)
                self.ResultList.append(data)
                self.driver.back()
            dp=pd.DataFrame(self.ResultList,columns=self.title)
            dp.to_excel("./"+self.school+".xlsx")
            if ll!=1:
                self.driver.back()
            ll+=1
        dp = pd.DataFrame(self.ResultList, columns=self.title)
        dp.to_excel('./人才-' + self.school + '.xlsx')

if __name__ == '__main__':
    # 在职教师
    one_url = 'http://pgi.ruc.edu.cn/zzjg/gltd/index.htm'
    # 学校
    school = '人民大学-中国人民大学公共治理研究院'
    demo = RenminUniversityNo53(one_url, school)
    demo.start()
