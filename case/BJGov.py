import pandas as pd, time, logging, colorlog,requests,json,re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class BJGov(object):
    def __init__(self, one_url, school):
        self.one_url = one_url
        self.school = school
        # 表头
        self.title = ['标题', '内容','时间']
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
        self.driver = webdriver.Chrome(options=self.options())
        #打开第一页
        self.driver.get(self.one_url)
        number=self.driver.find_element(By.XPATH,'//span[@class="u_page" and contains(text(),"共")]').text
        print(number)
        maximum=number.split("共")[1].split("页")[0]
        print(maximum)
        for m in range(0,int(maximum)+1):
            print(m)
            if m==0:
                url=self.driver.current_url
                self.driver.get(url)
            else:
                # self.driver.get("https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/zxxxi/index_"+str(m)+".html")
                self.driver.get(one_url+"/index_"+str(m)+".html")
            counts=self.driver.find_elements(By.XPATH,'//li[@class="col-md"]//a')
            print(len(counts))
            for c in counts:
                time.sleep(1)
                title=c.get_attribute("title")
                times=c.find_element(By.XPATH,'../span').text
                href=c.get_attribute("href")
                html=requests.get(href,headers=self.headers)
                html=html.text
                last_slash_index = href.rfind('/')
                hrefs = href[:last_slash_index + 1]
                pattern = re.compile(r'(<img.*?src=.*?".*?)\.\/(.*?\.(jpg|png))')
                new_string = pattern.sub(r'\1'+hrefs+r'\2',html)
                data={}
                data['标题'] = title
                data['内容'] = new_string
                data['时间'] = times
                print(data)
                self.ResultList.append(data)
                # df = pd.DataFrame(self.ResultList, columns=self.title)
                # df.to_excel(self.school + '.xlsx')
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel(self.school + '.xlsx')
            print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel(self.school + '.xlsx')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    one_url = 'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/zxxxi/'
    # one_url = 'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/bjdt/'
    # one_url = 'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/jjyw/'
    # one_url = 'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/xy/'
    # 学校

    school = '京津冀-最新消息'
    # school = '京津冀-北京动态'
    # school = '京津冀-津冀要闻'
    # school = '京津冀-三地协议'
    demo = BJGov(one_url, school)
    demo.start()
