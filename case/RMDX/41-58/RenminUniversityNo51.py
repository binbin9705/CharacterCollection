import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class RenminUniversityNo51(object):
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
        self.driver.get(self.one_url)
        links = self.driver.find_elements(By.XPATH, '//*[@class="m_left_c"]//li')
        print("有" + str(len(links)) + "可跳转链接")
        ll = 1
        # 拿到所有类型循环
        for link in links:
            # 类型（先锁定类型）
            types = link.find_element(By.XPATH, './/a').text
            if ll != 1:
                # time.sleep(3)
                link.find_element(By.XPATH, './/a').click()
            counts = self.driver.find_elements(By.XPATH, '// *[ @class ="news_list clear"] // a')
            print("有" + str(len(counts)) + "条人才信息")
            #只拿前两条做调试
            if len(counts) != 0:
                for c in counts[:2]:
                    # 姓名/职称
                    name = c.find_element(By.XPATH, './/h4').text
                    if "副教授" in name:
                        name = name.split("副教授")[0]
                        title = '副教授'
                    elif "教授" in name:
                        name = name.split("教授")[0]
                        title = '教授'
                    elif "讲师" in name:
                        name = name.split("讲师")[0]
                        title = '讲师'
                    else:
                        name = name
                        title = name
                    print(name)
                    # 照片
                    photo = c.find_element(By.XPATH, './/img').get_attribute("src")
                    # 进详情
                    c.find_element(By.XPATH, './/h4').click()

                    # 进详情页后
                    # 研究领域
                    field = ''
                    # 荣誉称号
                    honor = ''
                    # 电话
                    phone = ''
                    # 邮箱
                    mailbox = ''
                    # 简介
                    introduces = self.driver.find_elements(By.XPATH, '//*[@class="m_news_c_c"]')
                    if len(introduces) != 0:
                        introduce = "\n".join(map(lambda e: e.text, introduces))
                        introduce = introduce.strip()
                    else:
                        introduce = ''
                    data = {}
                    data['姓名'] = name
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
                df = pd.DataFrame(self.ResultList, columns=self.title)
                df.to_excel('./人才-' + self.school + '.xlsx')
            if ll != 1:
                self.driver.back()
            ll += 1
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    # 在职教师
    one_url = 'http://deke.ruc.edu.cn/kytd/ztqk/index.htm'
    # 学校
    school = '人民大学-数据工程与知识工程教育部重点实验室'
    demo = RenminUniversityNo51(one_url, school)
    demo.start()
