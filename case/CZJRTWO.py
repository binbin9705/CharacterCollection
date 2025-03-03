import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class CZJRTWO(object):
    def __init__(self, one_url,school):
        self.one_url = one_url
        # self.two_url = two_url
        # self.three_url = three_url
        # self.four_url = four_url
        self.school=school
        # 表头
        self.title = ['姓名', '研究领域', '职称', '荣誉称号', '电话','邮箱','简介','照片','类型']
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
        # self.driver = webdriver.Chrome(options=self.options())
        self.driver = webdriver.Chrome()
        # 在职教师
        self.driver.get(self.one_url)
        for s in range(1,17):
            if s!=1:
                wei = 'p_next_d p_fun_d'
                whole = self.isElementPresent(by=By.CLASS_NAME, value=wei)
                if whole != True:
                    self.driver.find_element(By.PARTIAL_LINK_TEXT, '下页').click()
                else:
                    pass
            #获取当前页有多少人才信息 #li标签内容不为空且style属性值不等于"display:none;"
            elements = self.driver.find_elements(By.XPATH, '/html/body/div[4]/div/div[1]/div[2]/ul/li[not(@style) or @style!="display:none;"]')
            print("第"+str(s)+"页:"+str(len(elements)))
            for x in elements:
                x.click()
                #姓名
                name=self.driver.find_element(By.XPATH,'/html/body/div[4]/div/div[1]/div[2]/form/div[1]/div[2]/h3').text
                name = name.split("\n")[1]
                #职称
                title=self.driver.find_element(By.XPATH,'/html/body/div[4]/div/div[1]/div[2]/form/div[1]/div[2]/div/p[1]/span[1]').text
                title = title.split("：")[1]
                #电子邮箱
                mailbox=self.driver.find_element(By.XPATH,'/html/body/div[4]/div/div[1]/div[2]/form/div[1]/div[2]/div/p[2]/span[1]').text
                mailbox=mailbox.split("：")[1]
                #电话
                phone=self.driver.find_element(By.XPATH,'/html/body/div[4]/div/div[1]/div[2]/form/div[1]/div[2]/div/p[2]/span[2]').text
                phone = phone.split("：")[1]
                #教授简介#[normalize-space()]：对应元素下=p标签或p标签内标签有值的
                # p_s = self.driver.find_elements(By.XPATH, './/div[@class="v_news_content"]//p[text()[normalize-space()]]')
                p_s = self.driver.find_elements(By.XPATH, './/div[@class="v_news_content"]//p[normalize-space()]')
                area = '\n'.join(map(lambda e: e.text, p_s))
                self.driver.find_element(By.LINK_TEXT,'研究成果').click()
                #研究成果
                # p_ss=self.driver.find_elements(By.XPATH, './/div[@class="tabshow1-ly dn nr"]//p[text()[normalize-space()]]')
                p_ss=self.driver.find_elements(By.XPATH, './/div[@class="tabshow1-ly dn nr"]//p[normalize-space()]')
                areas = '\n'.join(map(lambda e: e.text, p_ss))
                #研究领域和荣誉称号从教授简介和研究成功中获取 先把两块内容一块拿出去
                areas = str(area + '\n' + areas)
                #照片
                photo = self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div[2]/form/div[1]/div[1]/img').get_attribute("src")
                data = {}
                data['姓名'] = name
                data['研究领域'] = areas
                data['职称'] = title
                data['荣誉称号'] = areas
                data['电话'] = phone
                data['邮箱'] = mailbox
                data['简介'] = area
                data['照片'] = photo
                data['类型'] = title
                self.ResultList.append(data)
                print(data)
                self.driver.back()
                continue
            print(self.ResultList)
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = 'http://sf.ruc.edu.cn/xzyj/szdw1/zzjs1.htm'
    #学校
    school='人民大学-财政金融学院'
    demo = CZJRTWO(one_url,school)
    demo.start()
