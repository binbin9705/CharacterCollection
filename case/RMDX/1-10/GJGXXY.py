import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class GJGXXY(object):
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

    def start(self):
        self.driver = webdriver.Chrome(options=self.options())
        # 在职教师
        self.driver.get(self.one_url)
        counts=self.driver.find_elements(By.XPATH,'//*[@id="main"]/div/menu/div/button[*]/a')
        print(len(counts))
        for x in counts:
            link=x.get_attribute("href")
            print(link)
            if link!='http://sis.ruc.edu.cn/szll/szgjzzx/index.htm':
                self.driver.get(link)
            count_2=self.driver.find_elements(By.XPATH,'//*[@id="xyjg_content_div"]/div[*]/div/div[1]/a')
            for c in count_2:
                # time.sleep(1)
                c.click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                # 姓名
                name = self.driver.find_element(By.XPATH,'//*[@id="main"]/section/div/div/article/div[1]/span').text
                #简介
                ps=self.driver.find_elements(By.XPATH,'//*[@id="main"]/section/div/div/article/div//p')
                topInfo='\n'.join(map(lambda e: e.text, ps))
                # 电话
                phone =''
                # 电子邮箱
                mailbox = ''
                # 照片
                photo = self.driver.find_elements(By.XPATH,'//*[@id="main"]/section/div//img')
                photo = '\n'.join(map(lambda e: e.get_attribute("src"), photo))
                types=self.driver.find_element(By.XPATH,'//*[@id="main"]/div[2]/div/a').text
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
                self.driver.switch_to.window(self.driver.window_handles[-1])
            if link != 'http://sis.ruc.edu.cn/szll/szgjzzx/index.htm':
                print("返回导航执行了")
                self.driver.back()
                # 切换到窗口里面
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = 'http://sis.ruc.edu.cn/szll/szgjzzx/index.htm'
    # types = '在岗教师'
    #学校
    school='人民大学-国际关系学院'
    demo = GJGXXY(one_url,school)
    demo.start()

