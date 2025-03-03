import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class SHYRK(object):
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
        count = ['1', '2', '3', '4']
        for x in count:
            print(x)
            # self.driver.find_element(By.LINK_TEXT,x).click()
            self.driver.get('http://ssps.ruc.edu.cn/index.php?s=/Index/teacher/cid/8/p/'+str(x)+'.html')
            counts=self.driver.find_elements(By.XPATH,'/html/body/div[2]/div[2]/div[3]/a[*]')
            print(len(counts))
            for c in counts:
                links=c.get_attribute("href")
                self.driver.get(links)
                # 姓名
                names = self.driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/table[1]/tbody/tr/td/h1').text
                name=names.split("教授")[0]
                #研究领域
                study=self.driver.find_elements(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/table[2]/tbody/tr/td[2]/*')
                study = '\n'.join(map(lambda e: e.text, study))
                # print(study)
                #职称
                title = self.driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/table[1]/tbody/tr/td/h1/font').text
                # print(title)
                #荣誉称号
                # 电话
                phone =''
                #简介
                topInfos=""
                ps=self.driver.find_elements(By.XPATH,'//*[@id="fadetab"]//a')
                for z in ps:
                    z.click()
                    p_s2=self.driver.find_elements(By.XPATH,'//*[@id="fadecon"]//div')
                    topInfo='\n'.join(map(lambda e: e.text, p_s2))
                    topInfos+=topInfo
                topInfos=topInfos.replace("\n", "")
                # 电子邮箱
                pss=self.driver.find_elements(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/table[*]')
                mailboxs='\n'.join(map(lambda e: e.text, pss))
                if str(mailboxs.replace("\n", "")).find("邮箱：")!=-1:
                    mailbox =str(mailboxs.replace("\n", "")).split("邮箱：")[1]
                else:
                    mailbox =''
                # 照片
                photo = self.driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div[1]/div[1]/img').get_attribute("src")
                data = {}
                data['姓名'] = name
                data['研究领域'] = study
                data['职称'] = title
                data['荣誉称号'] = topInfos
                data['电话'] = phone
                data['邮箱'] = mailbox
                data['简介'] = topInfos
                data['照片'] = photo
                data['类型'] = types
                self.ResultList.append(data)
                print(data)
                self.driver.back()
                time.sleep(1)
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = 'http://ssps.ruc.edu.cn/index.php?s=/Index/teacher/cid/8.html'
    types = '在岗教师'
    #学校
    school='人民大学-社会与人口学院'
    demo = SHYRK(one_url,school)
    demo.start()

