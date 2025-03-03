import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class qizhidao(object):
    def __init__(self, one_url,school):
        self.one_url = one_url
        # self.two_url = two_url
        # self.three_url = three_url
        # self.four_url = four_url
        self.school=school
        # 表头
        self.title = ['标题', '发布时间', '发布部门']
        self.ResultList = []  # 最终数据

    def options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")  # 规避监测selenium
        options.add_argument('--start-maximized')  # 全屏运行
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 取消chrome受自动控制提示
        # 关掉浏览器记住密码弹窗
        prefs = {"": ""}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option("prefs", prefs)
        # options.headless=True
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
        time.sleep(1)
        # 在职教师
        self.driver.get(self.one_url)
        time.sleep(5)
        counts = self.driver.find_elements(By.XPATH, "//a[@class='search-list-scope']")
        print(len(counts))
        # for c in range(0, int(len(counts)-1)):
        for c in range(1, int(len(counts))+1):
            time.sleep(1)
            #标题
            # titles=self.driver.find_elements(By.XPATH,"//a[@class='search-list-scope']/*")
            titles=self.driver.find_elements(By.XPATH,"//a[@class='search-list-scope']["+str(c)+"]/div[1]")
            title = '\n'.join(map(lambda e: e.text, titles))
            print(title)
            #发布时间
            times=self.driver.find_elements(By.XPATH,"//a[@class='search-list-scope']["+str(c)+"]/div[5]")
            timedata = '\n'.join(map(lambda e: e.text, times))
            print(timedata)
            #发布部门
            departments = self.driver.find_elements(By.XPATH, "//a[@class='search-list-scope']["+str(c)+"]/div[6]")
            department = '\n'.join(map(lambda e: e.text, departments))
            print(department)
            data = {}
            data['标题'] = title
            data['发布时间'] = timedata
            data['发布部门'] = department
            self.ResultList.append(data)
            print(data)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        print(self.ResultList)
        df.to_excel('./人才-' + self.school + '.xlsx')

        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = 'https://zhengce.qizhidao.com/file/all/?keyword=%E4%BF%A1%E5%88%9B&source=home'
    #学校
    school='企知道'
    demo = qizhidao(one_url,school)
    demo.start()
