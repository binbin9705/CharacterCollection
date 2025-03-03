import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class CharacterCollection(object):
    def __init__(self, first_url, second_url, third_url,school):
        self.first_url = first_url
        self.second_url = second_url
        self.third_url = third_url
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
        # 进入类型一
        self.driver.get(self.first_url)
        WebDriverWait(self.driver, 10).until(EC.title_is("国际重要奖励获得者-清华大学"))
        #获取有多少条人才信息
        num = self.driver.execute_script("return document.querySelectorAll('.names').length")
        print("类型一，共"+str(num)+"条人才信息")
        for x in range(1, int(num) + 1):
            #职称、类型
            title=self.driver.find_element(By.XPATH,'/html/body/div[4]/div/div/p/a[4]').text
            self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[2]/div[2]/dl["+str(x)+"]/div/dd/a").click()
            #姓名
            name=self.driver.find_element(By.XPATH,'/html/body/div[5]/div/div[2]/div/form/div[1]/div[2]/h4').text
            #研究领域、荣誉称号、简介
            area=self.driver.find_element(By.XPATH,'//*[@id="vsb_content"]/div/p').text
            #照片
            photo=self.driver.find_element(By.XPATH,'/html/body/div[5]/div/div[2]/div/form/div[1]/div[1]/img').get_attribute("src")
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
            #返回上一页
            self.driver.back()
            continue
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        # self.driver.quit()
        time.sleep(1)
        #进入类型二
        self.driver.get(self.second_url)
        # 获取有多少条人才信息
        elements=self.driver.find_element(By.XPATH,'//*[@id="teacherSlide"]/div/div/div/ul').find_elements(By.XPATH,'./*')
        print("类型二，共" + str(len(elements)) + "条人才信息")
        for x in range(1, int(len(elements)) + 1):
            #职称、类型
            title=self.driver.find_element(By.XPATH,'/html/body/div[5]/div/div[2]/div[2]/div/div[1]/div[1]/p/a').text
            #人才详情页
            link=self.driver.find_element(By.XPATH, '//*[@id="teacherSlide"]/div/div/div/ul/li['+str(x)+']/a').get_attribute("href")
            print(link)
            self.driver.get(link)
            #姓名
            name=self.driver.find_element(By.XPATH,'/html/body/div[5]/div/div[2]/div/form/div[1]/div[2]/h4').text
            # 研究领域、荣誉称号、简介
            element=self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div').find_elements(By.XPATH,'./*')
            if len(element)==4:
                area1=self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[1]').text
                area2=self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[2]').text
                area3=self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[3]').text
                area4=self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[4]').text
                area =str(area1+'\n'+area2+'\n'+area3+'\n'+area4)
                print(area)
            elif len(element)==3:
                area1 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[1]').text
                area2 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[2]').text
                area3 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[3]').text
                area = str(area1 + '\n' + area2 + '\n' + area3)
                print(area)
            elif len(element)==2:
                area1 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[1]').text
                area2 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[2]').text
                area = str(area1 + '\n' + area2)
                print(area)
            elif len(element)==5:
                area1 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[1]').text
                area2 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[2]').text
                area3 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[3]').text
                area4 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[4]').text
                area5 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[5]').text
                area = str(area1 + '\n' + area2 + '\n' + area3 + '\n' + area4 + '\n' + area5)
                print(area)
            elif len(element)==1:
                area = self.driver.find_element(By.XPATH,'//*[@id="vsb_content"]/div/p').text
                print(area)
            else:
                area="--"
            photo=self.driver.find_element(By.XPATH,'/html/body/div[5]/div/div[2]/div/form/div[1]/div[1]/img').get_attribute("src")
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
            continue
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        # self.driver.quit()
        time.sleep(1)
        # 进入类型三
        self.driver.get(self.third_url)
        # 获取有多少条人才信息
        elements = self.driver.find_element(By.XPATH, '//*[@id="teacherSlide"]/div/div/div/ul').find_elements(By.XPATH,
                                                                                                              './*')
        print("类型三，共" + str(len(elements)) + "条人才信息")
        for x in range(1, int(len(elements)) + 1):
            if x==4:
                continue
            # 职称、类型
            title = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/div[2]/div/div[1]/div[2]/p/a').text
            # 人才详情页
            link = self.driver.find_element(By.XPATH, '//*[@id="teacherSlide"]/div/div/div/ul/li[' + str(
                x) + ']/a').get_attribute("href")
            print(link)
            self.driver.get(link)
            # 姓名
            name = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/div/form/div[1]/div[2]/h4').text
            # 研究领域、荣誉称号、简介
            element = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div').find_elements(By.XPATH, './*')
            if len(element) == 4:
                #取集合所有
                # area1 = self.driver.find_elements(By.XPATH, '//*[@id="vsb_content"]/div/p')
                # print(area1)
                # area = '\n'.join(map(lambda e: e.text, area1))
                area1 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[1]').text
                area2 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[2]').text
                area3 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[3]').text
                area4 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[4]').text
                area = str(area1 + '\n' + area2 + '\n' + area3 + '\n' + area4)
                print(area)
            elif len(element) == 3:
                area1 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[1]').text
                area2 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[2]').text
                area3 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[3]').text
                area = str(area1 + '\n' + area2 + '\n' + area3)
                print(area)
            elif len(element) == 2:
                area1 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[1]').text
                area2 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[2]').text
                area = str(area1 + '\n' + area2)
                print(area)
            elif len(element) == 5:
                area1 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[1]').text
                area2 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[2]').text
                area3 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[3]').text
                area4 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[4]').text
                area5 = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p[5]').text
                area = str(area1 + '\n' + area2 + '\n' + area3 + '\n' + area4 + '\n' + area5)
                print(area)
            elif len(element) == 1:
                area = self.driver.find_element(By.XPATH, '//*[@id="vsb_content"]/div/p').text
                print(area)
            else:
                area = "--"
            photo = self.driver.find_element(By.XPATH,
                                             '/html/body/div[5]/div/div[2]/div/form/div[1]/div[1]/img').get_attribute(
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
            continue
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")
if __name__ == '__main__':
    #国际重要奖励获得者
    first_url = 'https://www.tsinghua.edu.cn/jyjx/szdw/gjzyjlhdz.htm'
    #中国科学院院士
    second_url = 'https://www.tsinghua.edu.cn/jyjx/szdw/lyys/zgkxyys.htm'
    #中国工程院院士
    third_url = 'https://www.tsinghua.edu.cn/jyjx/szdw/lyys/zggcyys.htm'
    #学校
    school='清华'
    demo = CharacterCollection(first_url, second_url, third_url,school)
    demo.start()
