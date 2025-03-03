import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class WGYXY(object):
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
        # 在职教师
        nums = ['yyx', 'ryx', 'eyx', 'dyx', 'fyx', 'xbyyx',
                'MTIjyzx', 'dxyyjxb', 'yjsyyjxb']
        for n in nums[8:9]:
            print(n)
            self.driver.get('http://fl.ruc.edu.cn/sy/szdw/zzjs/'+str(n)+'/index.htm')
            if n=='yyx':
                cuont=self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/div[2]//a')

                print(len(cuont))
            else:
                # cuont = self.driver.find_elements(By.XPATH, '/html/body/div[4]/div[2]/div[2]/div[2]/div[2]//a')
                cuont = self.driver.find_elements(By.XPATH, '/html/body/div[4]/div[2]/div[2]/div[2]//a')
                print(len(cuont))
            for x in cuont:
                link=x.get_attribute('href')
                print(link)
                # 姓名
                name = x.find_element(By.XPATH,'..//h2').text
                # print(name)
                # self.driver.get(link)
                x.click()
                title = self.driver.find_element(By.XPATH,'//span[contains(text(),"职　称：")]').text
                lens=title.split("职　称：")
                if len(lens)!=0:
                    title = title.split("职　称：")[1]
                else:
                    title=''
                field=self.driver.find_elements(By.XPATH,'//h2[contains(text(),"研究专长")]/following-sibling::*')
                field='\n'.join(map(lambda e:e.text,field))
                if '学术职称'in field:
                    field=field.split('学术职称')[0]
                mailbox = self.driver.find_element(By.XPATH, '//span[contains(text(),"邮　箱：")]').text
                mailboxs = mailbox.split("邮　箱：")
                if len(mailboxs) != 0:
                    mailbox = mailbox.split("邮　箱：")[1]
                else:
                    mailbox = ''
                topInfo1=self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1][normalize-space()]')
                # print(len(topInfo1))
                topInfo=""
                if len(topInfo1)!=0:
                    topInfo1=self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]//*')
                    topInfo1='\n'.join(map(lambda e:e.text,topInfo1))
                    topInfo+= '\n' +topInfo1
                topInfo2 = self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2][normalize-space()]')
                if len(topInfo2) != 0:
                    self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[1]/a[2]').click()
                    topInfo2=self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]//*')
                    topInfo2 = '\n'.join(map(lambda e: e.text, topInfo2))
                    topInfo += '\n' +topInfo2
                topInfo3=self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div[3][normalize-space()]')
                if len(topInfo3)!=0:
                    self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[1]/a[3]').click()
                    topInfo3=self.driver.find_elements(By.XPATH,'/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div[3]//*')
                    topInfo3='\n'.join(map(lambda e:e.text,topInfo3))
                    topInfo += '\n' +topInfo3
                # print(topInfo)
                photo = self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div[2]//img').get_attribute("src")
                data = {}
                data['姓名'] = name
                data['研究领域'] = field
                data['职称'] = title
                data['荣誉称号'] = ''
                data['电话'] = ''
                data['邮箱'] = mailbox
                data['简介'] = topInfo
                data['照片'] = photo
                data['类型'] ='在职教师'
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
    one_url = 'http://art.ruc.edu.cn/szdw/szqk.htm'
    # 学校
    school = '人民大学-外国语学院'
    demo = WGYXY(one_url, school)
    demo.start()
