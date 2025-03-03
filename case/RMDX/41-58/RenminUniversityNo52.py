import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class RenminUniversityNo52(object):
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
        '''
        1.分类型进详情页
        :return:
        '''
        self.driver = webdriver.Chrome(options=self.options())
        self.driver.get(self.one_url)
        show_name = self.driver.find_elements(By.XPATH, '//div[@class="teach_team"]//div[@class="show_name"]')
        print(show_name)
        print(len(show_name))
        # //div[@class="teach_team"]//div[@class="show_name"]/following-sibling::*[1]
        cc = 1
        for s in show_name:
            types=s.find_element(By.XPATH,'.//p').text
            title = s.find_element(By.XPATH,'.//p').text
            conuts = s.find_elements(By.XPATH, './following-sibling::*[1]//a')
            # print(conuts)
            # print(len(conuts))
            print("第" + str(cc) + "次")
            cc += 1
            for c in conuts:
                time.sleep(2)
                name = c.find_element(By.XPATH, './/div[contains(@class,"name_box")]').text
                print(name)
                c.find_element(By.XPATH, './/div[contains(@class,"name_box")]').click()
                # 照片
                photos = self.driver.find_elements(By.XPATH, '//img')
                if (photos) != 0:
                    photo = '\n'.join(map(lambda p: p.get_attribute("src"), photos))
                else:
                    photo = ''
                # 简介
                introduces = self.driver.find_elements(By.XPATH, '//div[@class="teach_name"]/following-sibling::*')
                if len(introduces) != 0:
                    introduce = '\n'.join(map(lambda p: p.text, introduces))
                else:
                    introduce = ''
                field=''
                honor=''
                mailbox=''
                phone=''
                data={}
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
            df = pd.DataFrame(data=self.ResultList,columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')
        print(self.ResultList)
        df = pd.DataFrame(data=self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')



if __name__ == '__main__':
    # 在职教师
    one_url = 'http://iei.ruc.edu.cn/xygk/zzjg/index.htm'
    # 学校
    school = '人民大学-中国人民大学创业学院'
    demo = RenminUniversityNo52(one_url, school)
    demo.start()
