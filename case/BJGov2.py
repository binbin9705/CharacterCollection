import pandas as pd, time, logging, colorlog, requests, json, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook

class BJGovTwo(object):
    def __init__(self, one_urllist, schoollist):
        self.one_url = one_urllist
        self.school = schoollist
        # 表头
        self.title = ['标题', '内容', '时间']
        self.ResultList = []  # 最终数据
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

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
        # # 创建一个新的Excel文件
        # writer = pd.ExcelWriter('output.xlsx')
        # # 创建第一个DataFrame对象
        # data = {'列名': ['1','2']}
        # df1 = pd.DataFrame(data)
        # # 创建第二个DataFrame对象
        # data = {'列名': ['3','4']}
        # df2 = pd.DataFrame(data)
        # # 将第一个DataFrame写入第一个工作表
        # df1.to_excel(writer, sheet_name='23')
        # # 将第二个DataFrame写入第二个工作表
        # # df2.to_excel(writer, sheet_name='2', index=False)
        # df2.to_excel(writer, sheet_name='2')
        # # 关闭Excel文件
        # writer.save()
        # # writer.close()
        # writer = pd.ExcelWriter('循环.xlsx')
        # title = ['第一列', '第二列']
        # datas = []
        # a = 0
        # for s in ('one','two'):
        #     a+=1
        #     b='b'
        #     data={}
        #     data['第一列']=a
        #     data['第二列']=b
        #     datas.append(data)
        #     pd.DataFrame(datas,columns=title).to_excel(writer,sheet_name=s,index=False)
        #     datas.clear()
        #     # df=pd.DataFrame(data)
        #     # df.to_excel(writer,sheet_name=s)
        # writer.save()
        href='https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/jjyw/202404/t20240407_3610435.html'
        # href='1/2/3/45/6'
        indexhref=href.rfind('/')
        print(indexhref)
        #切片
        hrefs = href[:indexhref+1]
        print(hrefs)
        pattern = re.compile(r'(<img.*?src=.*?".*?)\.\/(.*?\.(jpg|png))')

if __name__ == '__main__':
    one_urllist = ['https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/zxxxi/',
                   # 'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/bjdt/',
                   # 'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/jjyw/',
                   'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/xy/']
    # one_url = 'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/zxxxi/'
    # one_url = 'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/bjdt/'
    # one_url = 'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/jjyw/'
    # one_url = 'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/xy/'
    # schoollist=['京津冀-最新消息','京津冀-北京动态','京津冀-津冀要闻','京津冀-三地协议']
    schoollist=['京津冀-最新消息','京津冀-三地协议']
    # school = '京津冀-三地协议'
    # school = '京津冀-最新消息'
    # school = '京津冀-北京动态'
    # school = '京津冀-津冀要闻'
    demo = BJGovTwo(one_urllist, schoollist)
    demo.start()
