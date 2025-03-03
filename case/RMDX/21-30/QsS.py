import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class QsS(object):
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
        nums=self.driver.find_elements(By.XPATH,"//a[contains(text(),'更多')]")
        for n in nums:
            n.click()
            counts=self.driver.find_elements(By.XPATH,'//td[@class="bkl4c"]//a')
            print(len(counts))
            for c in counts:
                # 姓名
                name=c.text
                print(name)
                c.click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                #简介
                time.sleep(0.3)
                introduces=self.driver.find_elements(By.XPATH,'//td[@class="info"]')

                if len(introduces)!=0:
                    introduce = '\n'.join(map(lambda e: e.text, introduces))
                    introduce = introduce.strip()
                else:
                    introduce=''
                photos=self.driver.find_elements(By.XPATH,'//td[@class="info"]//img')
                if len(photos)!=0:
                    photo= '\n'.join(map(lambda e: e.get_attribute("src"), photos))
                else:
                    photo=''

                field=''
                title=''
                honor=''
                phone=''
                mailboxs=self.driver.find_elements(By.XPATH,'//*[contains(text(),"邮箱")]')
                if len(mailboxs)!=0:
                    mailbox= '\n'.join(map(lambda e: e.text, mailboxs))
                else:
                    mailbox=''
                #类型
                types=self.driver.find_element(By.XPATH,'/html/body/table[3]/tbody/tr/td/a[3]').text
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
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[-1])
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
    one_url = 'http://iqh.ruc.edu.cn/bsxr/index.htm'
    # 学校
    school = '人民大学-清史所'
    demo = QsS(one_url, school)
    demo.start()
