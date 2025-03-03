import pandas as pd, time, logging, colorlog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class LigongUniversityNo09(object):
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

    def start(self):
        self.driver = webdriver.Chrome(options=self.options())
        for link in self.one_url:
            self.driver.get(link)
            counts=self.driver.find_elements(By.XPATH,'//*[@class="direbottom"]//li')
            print(len(counts))
            for c in counts:
                name=c.find_element(By.XPATH,'.//a//div[@class="namet gp-f16"]').text
                title=c.find_element(By.XPATH,'.//a//div[@class="nemws gp-f14"]').text
                print(name)
                print(title)
                #进详情
                c.find_element(By.XPATH,'.//a').click()
                time.sleep(0.5)
                photos=self.driver.find_elements(By.XPATH,'//div[@class="introduction"]//img')
                if len(photos)!=0:
                    photo='\n'.join(map(lambda e:e.get_attribute("src"),photos))
                else:
                    photo=''
                typess = self.driver.find_elements(By.XPATH, '//div[@class="gp-bread"]//a[4]')
                if len(typess)!=0:
                    types='\n'.join(map(lambda e:e.text,typess))
                else:
                    types=''
                introduces=self.driver.find_elements(By.XPATH,'//div[@class="introduction"]')
                if len(introduces)!=0:
                    introduce = '\n'.join(map(lambda e: e.text, introduces))
                    introduce=introduce.replace(' ', '')
                    introduce=introduce.split("ALL\n")[1]
                else:
                    introduce = ''
                # print(introduce)
                if "研究方向：" in introduce:
                    field = introduce.split("研究方向：")[1].split("\n")[0]
                elif "研究方向\n" in introduce:
                    field = introduce.split("研究方向\n")[1].split("\n")[0]
                else:
                    field = ''
                # if "职称\n" in introduce:
                #     title = introduce.split("职称\n")[1].split("\n")[0]
                # elif"职称：" in introduce:
                #     title = introduce.split("职称：")[1].split("\n")[0]
                # elif"职　　称" in introduce:
                #     title = introduce.split("职　　称")[1].split("\n")[0]
                # elif "职称" in introduce:
                #     title = introduce.split("职称")[1].split("\n")[0]
                # else:
                #     title = ''
                if "(Telephone)\n" in introduce:
                    phone = introduce.split("(Telephone)\n")[1].split("\n")[0]
                    if "010-"not in phone:
                        phone=''
                elif "办公电话\n" in introduce:
                    phone = introduce.split("办公电话\n")[1].split("\n")[0]
                    if "010-" not in phone:
                        phone=''
                elif "办公电话" in introduce:
                    phone = introduce.split("办公电话")[1].split("\n")[0]
                    if "010-"not in phone:
                        phone=''
                elif "联系电话：" in introduce:
                    phone = introduce.split("联系电话：")[1].split("\n")[0]
                    if "010-"not in phone:
                        phone=''
                else:
                    phone = ''
                if "E-mail："in introduce:
                    mailbox = introduce.split("E-mail：")[1].split("\n")[0]
                elif "(Email)\n" in introduce:
                    mailbox = introduce.split("(Email)\n")[1].split("\n")[0]
                    if "@"not in mailbox:
                        mailbox=''
                elif "邮件：" in introduce:
                    mailbox = introduce.split("邮件：")[1].split("\n")[0]
                    if "办公电话" in mailbox:
                        mailbox=mailbox.split("办公电话")[0]
                elif "邮件\n" in introduce:
                    mailbox = introduce.split("邮件\n")[1].split("\n")[0]
                    if "@"not in mailbox:
                        mailbox=''
                elif "邮件" in introduce:
                    mailbox = introduce.split("邮件")[1].split("\n")[0]
                    if "@"not in mailbox:
                        mailbox=''
                elif "邮箱：" in introduce:
                    mailbox = introduce.split("邮箱：")[1].split("\n")[0]
                    if "@"not in mailbox:
                        mailbox=''
                elif "邮箱" in introduce:
                    mailbox = introduce.split("邮箱")[1].split("\n")[0]
                    if "@"not in mailbox:
                        mailbox=''
                elif "邮　　箱" in introduce:
                    mailbox = introduce.split("邮　　箱")[1].split("\n")[0]
                    if "@"not in mailbox:
                        mailbox=''
                else:
                    mailbox = ''
                data = {}
                data['姓名'] = name
                data['研究领域'] = field
                data['职称'] = title
                # data['荣誉称号'] = honor
                data['荣誉称号'] = ''
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
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx')
        self.driver.quit()
        print("完成")

if __name__ == '__main__':
    #在职教师
    one_url = [
        'https://physics.bit.edu.cn/szdw/szml/zgjzc/ALL/index.htm',
        'https://physics.bit.edu.cn/szdw/szml/fgjzc/ALL_01/index.htm',
        'https://physics.bit.edu.cn/szdw/szml/fgjzc/ALL_01/index1.htm',
        'https://physics.bit.edu.cn/szdw/szml/zjzc/ALL_02/index.htm',
        'https://physics.bit.edu.cn/szdw/szml/zjzc/ALL_02/index1.htm',
        'https://physics.bit.edu.cn/szdw/szml/zzsyry/ALL_03/index.htm',
        'https://physics.bit.edu.cn/szdw/szml/dxwljxysyzx/ALL2022/index.htm',
    ]
    #学校
    school='北京理工大学-物理学院'
    demo = LigongUniversityNo09(one_url,school)
    demo.start()
