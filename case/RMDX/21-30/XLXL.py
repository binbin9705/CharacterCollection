import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class XLXL(object):
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
        nums=['js_sz','fjs','js']
        for n in nums:
            self.driver.get("http://psy.ruc.edu.cn/szdw/"+str(n)+"/index.htm")
            counts = self.driver.find_elements(By.XPATH, '//ul[@class="js_list"]//li')
            print(len(counts))
            for c in counts:
                #姓名
                name=c.find_element(By.XPATH,'.//strong').text
                print(name)
                #研究领域
                field=c.find_element(By.XPATH,'.//p').text
                field=field.split(name)[1].split("READ MORE >")[0]
                field = field.strip()
                #照片
                photos=c.find_elements(By.XPATH,'//img')
                if len(photos)!=0:
                    photo = '\n'.join(map(lambda e: e.get_attribute("src"), photos))
                else:
                    photo=''
                #进详情
                c.find_element(By.XPATH,'.//a[@class="readmore"]').click()
                time.sleep(0.5)
                #简介
                introduces=self.driver.find_elements(By.XPATH,'//div[@class="ntinfo_tit clearfix"]/following-sibling::*')
                if len(introduces)!=0:
                    introduce='\n'.join(map(lambda e:e.text,introduces))
                    introduce=introduce.strip()
                else:
                    introduce=''
                #职称
                title=self.driver.find_element(By.XPATH,'//div[@class="ntinfo_tit clearfix"]/following-sibling::*[1]').text
                #荣誉称号
                honor=''
                #电话
                phone=''
                #邮箱
                mailboxs=self.driver.find_elements(By.XPATH,'//span[contains(text(),"E-mail：")]')
                if len(mailboxs)!=0:
                    mailbox = '\n'.join(map(lambda e: e.text, mailboxs))
                else:
                    mailbox=''
                #类型
                types=self.driver.find_element(By.XPATH,'//a[@class="cur"]').text
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
    one_url = 'http://psy.ruc.edu.cn/szdw/js_sz/index.htm'
    # types='教师队伍'
    # 学校
    school = '人民大学-心理学系'
    demo = XLXL(one_url, school)
    demo.start()
