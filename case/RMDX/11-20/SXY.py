import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class SXY(object):
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
        for n in range(8,18):
            print(n)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '/html/body/div[5]/div/input[1]').clear()
            self.driver.find_element(By.XPATH,'/html/body/div[5]/div/input[1]').send_keys(n)

            self.driver.find_element(By.XPATH,'/html/body/div[5]/div/input[2]').click()
            counts = self.driver.find_elements(By.XPATH, '/html/body/div[4]/div/ul//a')
            print(len(counts))
            for c in counts:
                #照片
                photo=c.find_element(By.XPATH,'.//img').get_attribute('src')
                #姓名
                name=c.find_element(By.XPATH,'./em[2]/span[1]/i[1]').text
                #职称
                title=c.find_element(By.XPATH,'./em[2]/span[1]/i[2]').text
                #研究领域
                field = c.find_element(By.XPATH, './/span[contains(text(),"研究方向")]').text
                if"讲授课程" in field:
                    field=field.split("讲授课程")[0]
                print(c.get_attribute('href'))
                self.driver.get(c.get_attribute('href'))
                #简介
                introduce=self.driver.find_elements(By.XPATH,'/html/body/div[4]/div/div[2]/div[*]')
                if len(introduce) != 0:
                    introduce = '\n'.join(map(lambda e: e.text, introduce))
                else:
                    introduce=''
                # print(introduce)
                # 邮箱
                mailboxs = self.driver.find_elements(By.XPATH, '//span[contains(text(),"邮箱：")]')
                if len(mailboxs) != 0:
                    mailboxs = '\n'.join(map(lambda e: e.text, mailboxs))
                    mailbox = mailboxs.split("邮箱：")[1]
                else:
                    mailbox = ""
                # 联系方式
                phones = self.driver.find_elements(By.XPATH, '//span[contains(text(),"电话：")]')
                if len(phones) != 0:
                    phones = '\n'.join(map(lambda e: e.text, phones))
                    phone = phones.split("电话：")[1]
                else:
                    phone = ""
                #荣誉称号
                honor1 = self.driver.find_elements(By.XPATH, '/html/body/div[4]/div/div[2]/div[5]/div[2]//span[text()[normalize-space()]]')
                if len(honor1)!=0:
                    honor='\n'.join(map(lambda e:e.text,honor1))
                else:
                    honor=''
                data = {}
                data['姓名'] = name
                data['研究领域'] = field
                data['职称'] = title
                data['荣誉称号'] = honor
                data['电话'] = phone
                data['邮箱'] = mailbox
                data['简介'] = introduce
                data['照片'] = photo
                data['类型'] ='全职教师'
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
    # 全职教师
    one_url = 'https://www.rmbs.ruc.edu.cn/szyky/sz/qzjs/index.htm'
    # 学校
    school = '人民大学-商学院s'
    demo = SXY(one_url, school)
    demo.start()
