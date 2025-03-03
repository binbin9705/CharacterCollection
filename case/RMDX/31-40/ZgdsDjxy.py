import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class ZgdsDjxy(object):
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
        nums=['jys1/qb/index.htm','jys2/qb2/index.htm','jys3/qb3/index.htm']
        for n in nums:
            link="http://dsdj.ruc.edu.cn/szll/"+n
            print(link)
            self.driver.get(link)
            counts=self.driver.find_elements(By.XPATH,'//div[@class="teacherList"]//a')
            print(len(counts))
            for c in counts:
                c.find_element(By.XPATH,'.//p').click()
                name=self.driver.find_element(By.XPATH,'//div[@class="teacherBaseTxt"]//h6').text
                print(name)
                fields=self.driver.find_elements(By.XPATH,'//*[contains(text(),"研究方向")]')
                if len(fields) != 0:
                    field = '\n'.join(map(lambda e: e.text, fields))
                else:
                    field = ''
                titles=self.driver.find_elements(By.XPATH,'//*[contains(text(),"职称")]')
                if len(titles) != 0:
                    title = '\n'.join(map(lambda e: e.text, titles))
                else:
                    title = ''
                honor=''
                phone=''
                mailboxs=self.driver.find_elements(By.XPATH,'//*[contains(text(),"电子信箱")]')
                if len(mailboxs) != 0:
                    mailbox = '\n'.join(map(lambda e: e.text, mailboxs))
                else:
                    mailbox = ''
                introduces=self.driver.find_elements(By.XPATH,'//div[@class="personMess"]')
                if len(introduces) != 0:
                    introduce = '\n'.join(map(lambda e: e.text, introduces))
                else:
                    introduce = ''
                photos=self.driver.find_elements(By.XPATH,'//div[@class="teacherBase"]//img')
                if len(photos) != 0:
                    photo = '\n'.join(map(lambda e: e.get_attribute("src"), photos))
                else:
                    photo = ''
                types=self.driver.find_element(By.XPATH,'//div[@class="crumbs"]//a[3]').text
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
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    # 在职教师
    one_url = 'http://sgg.ruc.edu.cn/ssfc/szdw/index.htm'
    # 学校
    school = '人民大学-中共党史党建学院'
    demo = ZgdsDjxy(one_url, school)
    demo.start()
