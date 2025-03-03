import pandas as pd, time, logging, colorlog, requests, json, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class BJGovNew(object):
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
        self.driver = webdriver.Chrome(options=self.options())
        #创建一个名为京津冀的excle
        writer = pd.ExcelWriter('京津冀.xlsx')
        for num in range(0,len(self.one_url)):
            # 访问每个链接
            self.driver.get(self.one_url[num])
            number = self.driver.find_element(By.XPATH, '//span[@class="u_page" and contains(text(),"共")]').text
            print(number)
            #总页数
            maximum = number.split("共")[1].split("页")[0]
            print(maximum)
            #根据总页循环
            for m in range(0, int(maximum) + 1):
            # for m in range(0, 2):
                print(m)
                if m == 0:
                    url = self.driver.current_url
                    self.driver.get(url)
                else:
                    #不是第一次循环代表不在第一页，拼链接进入对应的页码
                    self.driver.get(self.one_url[num] + "/index_" + str(m) + ".html")
                #每页条数
                counts = self.driver.find_elements(By.XPATH, '//li[@class="col-md"]//a')
                print(len(counts))
                #根据条数循环
                for c in counts:
                    time.sleep(1)
                    #标题
                    title = c.get_attribute("title")
                    #时间
                    times = c.find_element(By.XPATH, '../span').text
                    href = c.get_attribute("href")
                    html = requests.get(href, headers=self.headers)
                    html = html.text
                    # print(html)
                    #修改图片地址
                    last_slash_index = href.rfind('/')
                    hrefs = href[:last_slash_index + 1]
                    pattern = re.compile(r'(<img.*?src=.*?".*?)\.\/(.*?\.(jpg|png))')
                    #拼装成新的html
                    new_string = pattern.sub(r'\1' + hrefs + r'\2', html)
                    data = {}
                    data['标题'] = title
                    data['内容'] = new_string
                    data['时间'] = times
                    print(data)
                    #存入数组
                    self.ResultList.append(data)
                #创建DataFrame对象
                df = pd.DataFrame(self.ResultList, columns=self.title)
                #每爬完一页存入对应的sheet
                df.to_excel(writer,sheet_name=self.school[num])
            #爬完某一类清空数组
            self.ResultList.clear()
        #保存文件并关闭ExcelWriter对象
        writer.save()
        self.driver.quit()
        print("完成")
if __name__ == '__main__':
    # one_urllist = ['https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/zxxxi/',
    #                'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/bjdt/',
    #                'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/jjyw/',
    #                'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/xy/']
    one_urllist = ['https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/bjdt/']
    schoollist=['京津冀-北京动态']
    # schoollist=['京津冀-最新消息','京津冀-北京动态','京津冀-津冀要闻','京津冀-三地协议']
    demo = BJGovNew(one_urllist, schoollist)
    demo.start()
