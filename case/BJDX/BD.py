import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class CharacterCollection(object):
    def __init__(self, one_url, two_url, three_url,four_url,school):
        self.one_url = one_url
        self.two_url = two_url
        self.three_url = three_url
        self.four_url = four_url
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
        self.driver = webdriver.Chrome(options=self.options())
        # # 中国科学院院士
        # self.driver.get(self.one_url)
        # #获取有几个分类
        # element = self.driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[2]/div').find_elements(By.XPATH, './*')
        # print("有"+str(len(element))+"个分类")
        # #循环所有分类
        # for x in range(1, int(len(element)) + 1):
        #     self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div[2]/div/a['+str(x)+']').click()
        #     title2 = self.driver.find_element(By.XPATH,
        #                                       '/html/body/div[4]/div[2]/div/div[2]/div/a[' + str(x) + ']').text
        #     #拖到最底部-才能准确拿到当前分类有多少条人才信息
        #     time.sleep(0.5)
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     time.sleep(0.5)
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     time.sleep(0.5)
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     time.sleep(0.5)
        #     # 获取每个分类下有多少条人才信息
        #     element = self.driver.find_element(By.XPATH, '//*[@id="datalist"]').find_elements(By.XPATH, './*')
        #     print("第"+str(x)+"个分类有"+str(len(element))+"条人才信息")
        #     #根据人才条数循环
        #     for c in range(1, int(len(element)) + 1):
        #         #职称、类型
        #         title1=self.driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div/div/div[1]/a/div[2]').text
        #         title=str(title1+":"+title2)
        #         #获取人才链接并跳转
        #         link=self.driver.find_element(By.XPATH,'//*[@id="datalist"]/div['+str(c)+']/a').get_attribute("href")
        #         print(link)
        #         self.driver.get(link)
        #         #姓名
        #         name=self.driver.find_element(By.CLASS_NAME,'h1').text
        #         #研究领域、荣誉称号、简介
        #         area=self.driver.execute_script('return document.getElementsByClassName("txt")[7].innerText')
        #         #照片
        #         photo=self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div[1]/div[1]/img').get_attribute("src")
        #         data = {}
        #         data['姓名'] = name
        #         data['研究领域'] = area
        #         data['职称'] = title
        #         data['荣誉称号'] = area
        #         data['电话'] = ''
        #         data['邮箱'] = ''
        #         data['简介'] = area
        #         data['照片'] = photo
        #         data['类型'] = title
        #         self.ResultList.append(data)
        #         print(data)
        #         #返回上一页
        #         self.driver.back()
        #         self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #         time.sleep(0.5)
        #         self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #         time.sleep(0.5)
        #         self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #         time.sleep(0.5)
        #         continue
        #     df = pd.DataFrame(self.ResultList, columns=self.title)
        #     df.to_excel('./人才-' + self.school + '.xlsx')
        #     #拖到最顶部-到最顶部切换下一个分类
        #     self.driver.execute_script("document.documentElement.scrollTop=0")
        #     continue
        #
        # #中国工程院院士
        # self.driver.get(self.two_url)
        # #职称、类型
        # title=self.driver.find_element(By.CLASS_NAME,'fz40').text
        # # 拖到最底部-才能准确拿到当前分类有多少条人才信息
        # time.sleep(0.5)
        # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # time.sleep(0.5)
        # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # time.sleep(0.5)
        # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # time.sleep(0.5)
        # # 获取每个分类下有多少条人才信息
        # element = self.driver.find_element(By.XPATH, '//*[@id="datalist"]').find_elements(By.XPATH, './*')
        # print("中国工程院院士共有"+str(len(element))+"条人才信息")
        # # 根据人才条数循环
        # for c in range(1, int(len(element)) + 1):
        #     #获取人才链接并跳转
        #     link=self.driver.find_element(By.XPATH,'//*[@id="datalist"]/div['+str(c)+']/a').get_attribute("href")
        #     print(link)
        #     self.driver.get(link)
        #     #姓名
        #     name=self.driver.find_element(By.CLASS_NAME,'h1').text
        #     #研究领域、荣誉称号、简介
        #     area=self.driver.execute_script('return document.getElementsByClassName("txt")[7].innerText')
        #     #照片
        #     photo=self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div[1]/div[1]/img').get_attribute("src")
        #     data = {}
        #     data['姓名'] = name
        #     data['研究领域'] = area
        #     data['职称'] = title
        #     data['荣誉称号'] = area
        #     data['电话'] = ''
        #     data['邮箱'] = ''
        #     data['简介'] = area
        #     data['照片'] = photo
        #     data['类型'] = title
        #     self.ResultList.append(data)
        #     print(data)
        #     #返回上一页
        #     self.driver.back()
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     time.sleep(0.5)
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     time.sleep(0.5)
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     time.sleep(0.5)
        #     continue
        # df = pd.DataFrame(self.ResultList, columns=self.title)
        # df.to_excel('./人才-' + self.school + '.xlsx')
        #
        # #发展中国家科学院院士
        # self.driver.get(self.three_url)
        # #职称、类型
        # title=self.driver.find_element(By.CLASS_NAME,'fz40').text
        # # 拖到最底部-才能准确拿到当前分类有多少条人才信息
        # time.sleep(0.5)
        # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # time.sleep(0.5)
        # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # time.sleep(0.5)
        # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # time.sleep(0.5)
        # # 获取每个分类下有多少条人才信息
        # element = self.driver.find_element(By.XPATH, '//*[@id="datalist"]').find_elements(By.XPATH, './*')
        # print("发展中国家科学院院士共有"+str(len(element))+"条人才信息")
        # # 根据人才条数循环
        # for c in range(1, int(len(element)) + 1):
        #     #获取人才链接并跳转
        #     link=self.driver.find_element(By.XPATH,'//*[@id="datalist"]/div['+str(c)+']/a').get_attribute("href")
        #     print(link)
        #     self.driver.get(link)
        #     #姓名
        #     name=self.driver.find_element(By.CLASS_NAME,'h1').text
        #     #研究领域、荣誉称号、简介
        #     area=self.driver.execute_script('return document.getElementsByClassName("txt")[7].innerText')
        #     #照片
        #     photo=self.driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div[1]/div[1]/img').get_attribute("src")
        #     data = {}
        #     data['姓名'] = name
        #     data['研究领域'] = area
        #     data['职称'] = title
        #     data['荣誉称号'] = area
        #     data['电话'] = ''
        #     data['邮箱'] = ''
        #     data['简介'] = area
        #     data['照片'] = photo
        #     data['类型'] = title
        #     self.ResultList.append(data)
        #     print(data)
        #     #返回上一页
        #     self.driver.back()
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     time.sleep(0.5)
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     time.sleep(0.5)
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     time.sleep(0.5)
        #     continue
        # df = pd.DataFrame(self.ResultList, columns=self.title)
        # df.to_excel('./人才-' + self.school + '.xlsx')

        # 国家级教学名师
        self.driver.get(self.four_url)
        # 职称、类型
        title = self.driver.find_element(By.CLASS_NAME, 'fz40').text
        # 拖到最底部-才能准确拿到当前分类有多少条人才信息
        time.sleep(0.5)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(0.5)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(0.5)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(0.5)
        # 获取每个分类下有多少条人才信息
        element = self.driver.find_element(By.XPATH, '//*[@id="datalist"]').find_elements(By.XPATH, './*')
        print("国家级教学名师共有" + str(len(element)) + "条人才信息")
        # 根据人才条数循环
        for c in range(1, int(len(element)) + 1):
            # 获取人才链接并跳转
            link = self.driver.find_element(By.XPATH, '//*[@id="datalist"]/div[' + str(c) + ']/a').get_attribute("href")
            print(link)
            if link==None:
                continue
            else:
                self.driver.get(link)
                # 姓名
                name = self.driver.find_element(By.CLASS_NAME, 'h1').text
                # 研究领域、荣誉称号、简介
                area = self.driver.execute_script('return document.getElementsByClassName("txt")[7].innerText')
                # 照片
                photo = self.driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div[1]/img').get_attribute(
                    "src")
                data = {}
                data['姓名'] = name
                data['研究领域'] = area
                data['职称'] = title
                data['荣誉称号'] = area
                data['电话'] = ''
                data['邮箱'] = ''
                data['简介'] = area
                data['照片'] = photo
                data['类型'] = title
                self.ResultList.append(data)
                print(data)
                # 返回上一页
                self.driver.back()
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(0.5)
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(0.5)
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(0.5)
                continue
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')

        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")
if __name__ == '__main__':
    #中国科学院院士
    one_url = 'https://www.pku.edu.cn/mathScience.html'
    #中国工程院院士
    two_url = 'https://www.pku.edu.cn/academician.html'
    # 发展中国家科学院院士
    three_url = 'https://www.pku.edu.cn/developing_countries.html'
    # 国家级教学名师
    four_url = 'https://www.pku.edu.cn/national_famous_teacher.html'
    #学校
    school='北大'
    demo = CharacterCollection(one_url, two_url, three_url,four_url,school)
    demo.start()
