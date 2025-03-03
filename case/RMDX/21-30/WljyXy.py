import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class WljyXy(object):
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
        nums=[1,2,3,4,5,6,7,8]
        for n in nums:
            self.driver.get("http://www.cmr.com.cn/html/xljy/zszl/zysz/zyjs/list_124_"+str(n)+".html")
            counts=self.driver.find_elements(By.XPATH,'//div[@class="comm_person"]//li')
            print(len(counts))
            for c in counts:
                # 姓名
                name=c.find_element(By.XPATH,'.//a').text
                print(name)
                link=c.find_element(By.XPATH, './/a').get_attribute("href")
                c.find_element(By.XPATH, './/a').click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                #简介
                introduces1=self.driver.find_elements(By.XPATH,'//div[@id="tab_box"]')
                introduce1 = '\n'.join(map(lambda e: e.text, introduces1))
                time.sleep(0.3)
                if len(self.driver.find_elements(By.XPATH,'//li[contains(text(),"研究成果")]'))!=0:
                    self.driver.find_element(By.XPATH,'//li[contains(text(),"研究成果")]').click()
                    introduces2=self.driver.find_elements(By.XPATH,'//div[@id="tab_box"]')
                    introduce2 = '\n'.join(map(lambda e: e.text, introduces2))
                else:
                    introduce2=''
                introduce=introduce1+introduce2
                #照片
                photos=self.driver.find_elements(By.XPATH,'//div[@class="leftBox fl-left"]//img')
                if len(photos)!=0:
                    photo='\n'.join(map(lambda e:e.get_attribute("src"),photos))
                else:
                    photo=''
                field=''
                title=''
                honor=''
                phone=''
                mailbox=''
                #类型
                types='专业教师'
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
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    # 在职教师
    one_url = 'http://www.cmr.com.cn/html/xljy/zszl/zysz/zyjs/'
    # types='教师队伍'
    # 学校
    school = '人民大学-网络教育学院'
    demo = WljyXy(one_url, school)
    demo.start()
