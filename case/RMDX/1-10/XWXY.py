import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class XWXY(object):
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
        counts=self.driver.find_elements(By.XPATH,'/html/body/div[3]/div/ol//a[text()[normalize-space()]]')
        print(len(counts))
        for x in counts:
            # 姓名
            name = x.text
            types=x.find_element(By.XPATH,'/html/body/div[3]/div/ol//a[text()[normalize-space()]]/following-sibling::*[1]').text
            x.click()
            study1 = self.driver.find_elements(By.XPATH, '//p//*[contains(text(),"研究方向：")]/..')
            study = '\n'.join(map(lambda e: e.text, study1))
            if len(study1)!=0:
                study = study.split("研究方向：")[1]
            else:
                study =''
            titles=self.driver.find_elements(By.XPATH,'//p//*[contains(text(),"现任职务：")]/..')
            title = '\n'.join(map(lambda e: e.text, titles))
            if len(titles)!=0:
                if title=="现任职务：":
                    title = self.driver.find_element(By.XPATH, '//p//*[contains(text(),"现任职务：")]/../following-sibling::*[1]').text
                else:
                    title = title.split("现任职务：")[1]
            topInfo=self.driver.find_elements(By.XPATH,'//p//*[contains(text(),"学术成果：")]/..//following-sibling::*')
            topInfo = '\n'.join(map(lambda e: e.text, topInfo))
            phone=''
            mailbox1 = self.driver.find_elements(By.XPATH, '//*[contains(text(),"邮箱")]')
            if len(mailbox1) != 0:
                mailbox = '\n'.join(map(lambda e: e.text, mailbox1))
                # print(mailbox2)
            else:
                mailbox = ''
            photo=self.driver.find_element(By.XPATH,'//*[@id="teacher"]/div[3]/div/div[2]//img').get_attribute("src")
            data = {}
            data['姓名'] = name
            data['研究领域'] = study
            data['职称'] = title
            data['荣誉称号'] = topInfo
            data['电话'] = phone
            data['邮箱'] = mailbox
            data['简介'] = topInfo
            data['照片'] = photo
            data['类型'] = types
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
    one_url = 'http://jcr.ruc.edu.cn/zw/jzyg/js/index.htm'
    # types = '在职教师'
    #学校
    school='人民大学-新闻学院'
    demo = XWXY(one_url,school)
    demo.start()

