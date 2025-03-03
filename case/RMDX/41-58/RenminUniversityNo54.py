import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class RenminUniversityNo54(object):
    def __init__(self, one_url,school):
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
        nums=self.driver.find_elements(By.XPATH,'//*[@class="item"]//li')
        nums=self.driver.find_elements(By.XPATH,'//*[@class="item"][2]//li')
        # for n in nums:
        #     types=n.text
        #     print(types)
        #     links=n.find_elements(By.XPATH,'./..//ul//li')
        #     print(len(links))
        ll=1
        for l in nums:
            time.sleep(0.5)
            # if ll==11:
            #     ll += 1
            #     continue
            # name=l.find_element(By.XPATH,'.//h5').text
            name=self.driver.find_element(By.XPATH,'//*[@class="item"][2]//li['+str(ll)+']//h5').text
            print(name)
            # photo=l.find_element(By.XPATH,'.//img').get_attribute("src")
            photo=self.driver.find_element(By.XPATH,'//*[@class="item"][2]//li['+str(ll)+']//img').get_attribute("src")
            # title=l.find_element(By.XPATH,'.//p').text
            title=self.driver.find_element(By.XPATH,'//*[@class="item"][2]//li['+str(ll)+']//p').text
            # l.find_element(By.XPATH, './/h5').click()
            self.driver.find_element(By.XPATH, '//*[@class="item"][2]//li['+str(ll)+']//p').click()
            # 研究领域
            fields=self.driver.find_elements(By.XPATH,'//*[contains(text(),"研究领域") and @class="pra" ]')
            if len(fields)!=0:
                fields = self.driver.find_elements(By.XPATH, '//*[contains(text(),"研究领域") and @class="pra" ]//span')
                field='\n'.join(map(lambda e:e.text,fields))
            else:
                field=''
            maiboxs=self.driver.find_elements(By.XPATH,'//*[contains(text(),"E-mail") and @class="pra" ]')
            if len(maiboxs)!=0:
                maiboxs=self.driver.find_elements(By.XPATH,'//*[contains(text(),"E-mail") and @class="pra" ]//span')
                mailbox='\n'.join(map(lambda e:e.text,maiboxs))
            else:
                mailbox=''
            introduces=self.driver.find_elements(By.XPATH,'//*[@class="pra"][2]/following-sibling::*[1]')
            if len(introduces) != 0:
                introduce = '\n'.join(map(lambda e: e.text, introduces))
            else:
                introduce = ''
            honor=''
            phone=''
            types=''
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
            ll+=1
        print(self.ResultList)
        dp = pd.DataFrame(self.ResultList, columns=self.title)
        dp.to_excel('./人才-' + self.school + '.xlsx')

if __name__ == '__main__':
    # 在职教师
    one_url = 'http://rdcy.ruc.edu.cn/zw/yjtd/yjly/yjlyqb/index.htm'
    # 学校
    school = '人民大学-中国人民大学重阳金融研究院'
    demo = RenminUniversityNo54(one_url,school)
    demo.start()
