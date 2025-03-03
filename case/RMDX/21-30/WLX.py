import pandas as pd,json,time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class WLX(object):
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
        nums = ['.htm','/3.htm','/2.htm','/1.htm']
        for n in nums:
            self.driver.get("http://www.phys.ruc.edu.cn/szdw/jzry"+n+"")
            counts = self.driver.find_elements(By.XPATH, '//ul[@class="m2tcul clearfix"]//li')
            print(len(counts))
            for c in counts:
                time.sleep(1)
                #职称
                title=c.find_element(By.XPATH,'//div[@class="m2tcBom"]//span').text
                print(title)
                #进详情
                # c.click()
                self.driver.get(c.find_element(By.XPATH,'.//a').get_attribute("href"))
                time.sleep(2)
                names=self.driver.find_element(By.XPATH,'//div[@class="m3pLx"]//strong').text
                spans=self.driver.find_element(By.XPATH,'//div[@class="m3pLx"]//strong/span').text
                if spans in names:
                    name=names.split(spans)[0]
                # # 姓名
                # name = self.driver.find_element(By.XPATH, '/html/body/div[10]/div/div/a[6]').text
                print(name)
                #研究领域
                field=self.driver.find_element(By.XPATH,'/html/body/div[10]/div/div/a[5]').text
                # print(field)
                # 邮箱
                mailboxs =self.driver.find_elements(By.XPATH,'//*[contains(text(),"电子邮箱：")]')
                if len(mailboxs)!=0:
                    mailbox='\n'.join(map(lambda e: e.text, mailboxs))

                    mailbox = mailbox.split("电子邮箱：")[1]
                else:
                    mailbox=''
                #电话
                phones=self.driver.find_elements(By.XPATH,'//*[contains(text(),"电　　话：")]')
                if len(phones)!=0:
                    phone='\n'.join(map(lambda e:e.text,phones))
                    phone=phone.split("电　　话：")[1]
                else:
                    phone=''
                #荣誉称号
                honor=''
                #照片
                photos=self.driver.find_elements(By.XPATH,'//div[@class="m3pImgs"]//img')
                if len(photos)!=0:
                    photo='\n'.join(map(lambda e:e.get_attribute("src"),photos))
                else:
                    photo=''
                #类型
                types=self.driver.find_element(By.XPATH,'/html/body/div[10]/div/div/a[3]').text
                #简介
                introduces=self.driver.find_elements(By.XPATH,'//div[@id="vsb_content"]')
                introduce = '\n'.join(map(lambda e: e.text, introduces))
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
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")
if __name__ == '__main__':
    # 在职教师
    one_url = "http://www.phys.ruc.edu.cn/szdw/jzry.htm"
    # 学校
    school = '人民大学-物理系'
    demo = WLX(one_url, school)
    demo.start()
