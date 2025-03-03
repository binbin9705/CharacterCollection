import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class NyYncfzXY(object):
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
        self.driver.implicitly_wait(5)
        nums=['qzjs','fjs','zljs']
        for n in nums:
            self.driver.get('http://www.sard.ruc.edu.cn/szll/zzjs/' + n + '/index.htm')
            counts = self.driver.find_elements(By.XPATH, '//div[@class="teacherCont fl"]')
            print(len(counts))
            for c in counts:
                #姓名
                name=c.find_element(By.XPATH,'.//p').text
                #照片
                photo=c.find_element(By.XPATH,'.//img').get_attribute("src")
                #详情页链接
                link=c.find_element(By.XPATH,'.//a').get_attribute("href")
                print(link)
                self.driver.get(link)
                titles=self.driver.find_elements(By.XPATH,'//*[contains(text(),"职称：")]')
                if len(titles)!=0:
                    title='\n'.join(map(lambda e:e.text,titles))
                else:
                    title=''
                #研究领域
                fields=self.driver.find_elements(By.XPATH,'//*[contains(text(),"研究方向：")]')
                if len(fields) != 0:
                    field = '\n'.join(map(lambda e: e.text, fields))
                else:
                    field = ''
                #荣誉称号
                honor=''
                #电话
                phones=self.driver.find_elements(By.XPATH,'//*[contains(text(),"电话")]')
                if len(fields) != 0:
                    phone = '\n'.join(map(lambda e: e.text, phones))
                else:
                    phone = ''
                #邮箱
                mailboxs=self.driver.find_elements(By.XPATH,'//*[contains(text(),"email")]')
                if len(mailboxs) != 0:
                    mailbox = '\n'.join(map(lambda e: e.text, mailboxs))
                else:
                    mailbox = ''
                #简介
                introduces=self.driver.find_elements(By.XPATH,'//*[contains(text(),"个人简介")]/following-sibling::*[1]')
                if len(introduces) != 0:
                    introduce = '\n'.join(map(lambda e: e.text, introduces))
                else:
                    introduces1 = self.driver.find_elements(By.XPATH,'//*[contains(text(),"个人简介")]/../following-sibling::*[1]')
                    if len(introduces1) != 0:
                        introduce = '\n'.join(map(lambda e: e.text, introduces1))
                    else:
                        introduce=''
                #类型
                types=self.driver.find_element(By.XPATH,'//a[@href="index.htm"]').text
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
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    # 在职教师
    one_url = 'http://stat.ruc.edu.cn/jxtd/jsdw/index.htm'
    # types='教师队伍'
    # 学校
    school = '人民大学-农业与农村发展学院'
    demo = NyYncfzXY(one_url, school)
    demo.start()
