import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class TjYdsjYjy(object):
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


    def start(self):
        self.driver = webdriver.Chrome(options=self.options())
        nums=["index.htm","index1.htm","index2.htm"]
        for n in nums[1:]:
            link="http://isbd.ruc.edu.cn/sztd/"+n
            print(link)
            self.driver.get(link)
            counts=self.driver.find_elements(By.XPATH,'//div[@class="sztuandui clearfix"]//div')
            print(len(counts))
            for c in counts:
                # link=c.find_element(By.XPATH,'./a').get_attribute("href")

                name=c.find_element(By.XPATH,'.//font').text
                title=c.find_element(By.XPATH,'.//p[1]').text
                field=c.find_element(By.XPATH,'.//p[2]').text
                mailbox=c.find_element(By.XPATH,'.//p[3]').text
                photo=c.find_element(By.XPATH,'.//img').get_attribute("src")
                c.find_element(By.XPATH,'.//img').click()
                introduces=self.driver.find_elements(By.XPATH,'//div[@class="wuyshux"]')
                introduce='\n'.join(map(lambda e:e.text,introduces))
                data={}
                data['姓名'] = name
                data['研究领域'] = field
                data['职称'] = title
                data['荣誉称号'] = ''
                data['电话'] = ''
                data['邮箱'] = mailbox
                data['简介'] = introduce
                data['照片'] = photo
                data['类型'] ="在职教师"
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
    one_url = 'http://ipr.ruc.edu.cn/szll/qzjs.htm'
    # 学校
    school = '人民大学-统计与大数据研究院'
    demo = TjYdsjYjy(one_url, school)
    demo.start()
