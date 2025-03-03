import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class GjfaYzlyjy(object):
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
        nn=['"教授"','"研究员"','"副教授"','"讲师"']
        cc=1
        for c in range(1,6):
            print('//*[contains(text(),'+nn[1]+')]//a['+str(cc)+']')
            name = self.driver.find_element(By.XPATH, '//*[contains(text(),' + nn[0] + ')]//a[' + str(cc) + ']').text
            print(name)
            self.driver.find_element(By.XPATH,'//*[contains(text(),'+nn[0]+')]//a['+str(cc)+']').click()
            #研究领域
            field=''
            #职称
            title=''
            honor=''
            phone=''
            mailboxs=self.driver.find_elements(By.XPATH,'//*[contains(text(),"E-mail")]')
            if len(mailboxs)!=0:
                mailboxss=self.driver.find_elements(By.XPATH,'//*[contains(text(),"ail")]/..')
                mailbox="\n".join(map(lambda e:e.text,mailboxss))
            else:
                mailbox=''
            introduces=self.driver.find_elements(By.XPATH,'//*[@class="zi2"]//*')
            introduce = "\n".join(map(lambda e: e.text, introduces))
            photo=self.driver.find_element(By.XPATH,'//*[@class="div_img "]//img').get_attribute("src")
            types='全职教师'
            data={}
            data['姓名'] = name
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
            cc+=1
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    # 在职教师
    one_url = 'http://nads.ruc.edu.cn/jgsz/qzjs/index.htm'
    # 学校
    school = '人民大学-国家发展与战略研究院'
    demo = GjfaYzlyjy(one_url, school)
    demo.start()
