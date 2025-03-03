import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class GJXY_ZF(object):
    def __init__(self, one_url,school):
        self.one_url = one_url
        self.school=school
        # 表头
        self.title = ['姓名', '研究领域', '职称', '荣誉称号', '电话','邮箱','简介','照片','类型']
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
        self.driver.get(self.one_url)
        # count=self.driver.find_elements(By.XPATH,'/html/body/div/div[2]/div/div[1]/div[2]/ul/li[4]/div//a')
        # print(len(count))
        # for x in count:
        #     link=x.get_attribute("href")
        #     #类型、职称、研究方向
        #     types=x.text
        #     print(link)
        #     # self.driver.get(link)
        #     x.click()
        counts=self.driver.find_elements(By.XPATH,'/html/body/div/div[2]/div/div[2]/div[2]/div/div/table/tbody//a[not(@style)]')
        print(len(counts))
        for c in counts:
            # print(c)
            links=c.get_attribute("href")
            # 照片
            photo = c.find_element(By.XPATH,'//img').get_attribute("src")
            # print(photo)
            c.click()
            time.sleep(1)
            #切换到新窗口
            self.driver.switch_to.window(self.driver.window_handles[-1])
            # 姓名
            name = self.driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[2]/div/div/p').text
            # print(name)
            #简介
            p_sss=self.driver.find_elements(By.XPATH,'/html/body/div[1]/div[2]/div/div[2]/div[2]/div/div/span//p')
            topInfo='\n'.join(map(lambda e: e.text, p_sss))
            # print(topInfo)
            # 电子邮箱
            mailbox =''
            # 电话
            phone =''
            data = {}
            data['姓名'] = name
            data['研究领域'] = topInfo
            data['职称'] = types
            data['荣誉称号'] = topInfo
            data['电话'] = phone
            data['邮箱'] = mailbox
            data['简介'] = topInfo
            data['照片'] = photo
            data['类型'] = types
            self.ResultList.append(data)
            print(data)
            self.driver.close()
            #切换到窗口里面
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(1)
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    # one_url = 'http://ifc.ruc.edu.cn/xygk/szll/zfsz/index.htm'
    # one_url = 'http://ifc.ruc.edu.cn/xygk/szll/zfsz/ggksz/index.htm'
    # one_url = 'http://ifc.ruc.edu.cn/xygk/szll/zfsz/zyksz/index.htm'
    # one_url = 'http://ifc.ruc.edu.cn/xygk/szll/zfsz/fysz/index.htm'
    # one_url = 'http://ifc.ruc.edu.cn/xygk/szll/ffsz/index.htm'
    # one_url = 'http://ifc.ruc.edu.cn/xygk/szll/ffsz/fyzyksz/index.htm'
    one_url = 'http://ifc.ruc.edu.cn/xygk/szll/ffsz/fyfysz/index.htm'
    types = '法国院校派驻师资'
    #学校
    school='人民大学-国际学院（苏州研究院）-中法学院'
    demo = GJXY_ZF(one_url,school)
    demo.start()

