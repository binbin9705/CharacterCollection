import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class YSXY(object):
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
        for x in range(1,8):
            if x != 1:
                wei = 'p_last_d p_fun_d'
                whole = self.isElementPresent(by=By.CLASS_NAME, value=wei)
                if whole != True:
                    self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[3]/div[3]/span/span[10]/a').click()
                else:
                    pass
            counts=self.driver.find_elements(By.XPATH,'/html/body/div[2]/div/div[2]/div[3]/div/a[*]')
            print(len(counts))
            for c in counts:
                # 姓名
                name = c.text
                name=name.split(" ")[0]
                c.click()
                types=self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/ul/li[1]/ul/li[2]/a').text
                title=self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/form/div/div[2]/div[1]/p').text
                topInfo=self.driver.find_elements(By.XPATH,'//*[@id="vsb_content"]/div[*]')
                topInfo='\n'.join(map(lambda e:e.text,topInfo))
                photo=self.driver.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/form/div/div[1]/img').get_attribute("src")
                data = {}
                data['姓名'] = name
                data['研究领域'] = ''
                data['职称'] = title
                data['荣誉称号'] = ''
                data['电话'] = ''
                data['邮箱'] = ''
                data['简介'] = topInfo
                data['照片'] = photo
                data['类型'] = types
                self.ResultList.append(data)
                print(data)
                time.sleep(1)
                self.driver.back()
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = 'http://art.ruc.edu.cn/szdw/szqk.htm'
    #学校
    school='人民大学-艺术学院'
    demo = YSXY(one_url,school)
    demo.start()

