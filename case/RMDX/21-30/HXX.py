'''
学校:人民大学-化学系
地址:http://chem.ruc.edu.cn/szll/zzjs/index.htm
1.用123区分不同学科
    1=物质结构中心
    2=合成化学中心
    3=材料科学与工程中心
2.循环获取不同学科下有多少人-counts(是一组element)
3.循环拿不同学科人的信息-for c in counts:

//*[contains(text(),"电话")]-匹配页面包含文本值等于"电话"的元素(element)
following-sibling::*-获取相邻元素后面所有元素
'''

import pandas as pd,time
from selenium import webdriver
from selenium.webdriver.common.by import By



class HXX(object):
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

        nums=[1,2,3]
        for n in nums:
            counts = self.driver.find_elements(By.XPATH, '//ul[@class="row teacher-list"]['+str(n)+']/li/following-sibling::*')
            print(len(counts))
            for c in counts:
                #姓名
                name=c.find_element(By.XPATH,'.//span[@class="p14"]').text
                print(name)
                #类型
                types=c.find_element(By.XPATH,'./..//span[@class="title-english"]').text
                #照片
                photo=c.find_element(By.XPATH,'.//img').get_attribute("src")
                #进详情
                c.find_element(By.XPATH, './/img').click()
                #电话
                phones=self.driver.find_elements(By.XPATH,'//*[contains(text(),"电话")]')
                if len(phones)!=0:
                    phone='\n'.join(map(lambda e:e.text,phones))
                elif len(self.driver.find_elements(By.XPATH,'//*[contains(text(),"联系电话：")]'))!=0:
                    phone = '\n'.join(map(lambda e: e.text, self.driver.find_elements(By.XPATH,'//*[contains(text(),"联系电话：")]')))
                else:
                    phone=''
                #邮箱
                mailboxs=self.driver.find_elements(By.XPATH,'//*[contains(text(),"电子邮件")]')
                if len(mailboxs)!=0:
                    mailbox='\n'.join(map(lambda e:e.text,mailboxs))
                elif len(self.driver.find_elements(By.XPATH,'//*[contains(text(),"E-mail")]'))!=0:
                    mailbox = '\n'.join(map(lambda e: e.text, self.driver.find_elements(By.XPATH,'//*[contains(text(),"E-mail")]')))
                else:
                    mailbox=''
                # 职称
                title = ''
                # 简介
                introduces=self.driver.find_elements(By.XPATH,'//div[@class="col-sm-12 col-md-9 achievements-teacher"]')
                if len(introduces) != 0:
                    introduce='\n'.join(map(lambda e:e.text,introduces))
                    introduce=introduce.strip()
                else:
                    introduce=''
                # print(introduce)
                # 研究领域
                if "主要研究方向" in introduce:
                    field=introduce.split("主要研究方向：")[1].split("\n")[0]
                    if field=='':
                        field=introduce.split("主要研究方向：\n")[1].split("\n")[0]
                elif "研究方向\n"in introduce:
                    field = introduce.split("研究方向\n")[1].split("\n\n")[0]
                elif "主要研究领域:\n"in introduce:
                    field = introduce.split("主要研究领域:\n")[1].split("\n")[0]
                elif"主要研究领域：\n"in introduce:
                    field = introduce.split("主要研究领域：\n")[1].split("科研项目")[0]
                else:
                    field=''
                #荣誉称号
                honor=''
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
                self.driver.back()
            #每循环完一个学科就存到excle中
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx')
        #全部结束后存入excle
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    one_url = "http://chem.ruc.edu.cn/szll/zzjs/index.htm"
    # 学校
    school = '人民大学-化学系'
    demo = HXX(one_url, school)
    demo.start()
