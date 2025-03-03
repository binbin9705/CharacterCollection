import pandas as pd, time, logging, colorlog, requests, json
from selenium import webdriver
from selenium.webdriver.common.by import By


class NongyeUniversityNo01(object):
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
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 取消chrome受自动控制提示
        # 关掉浏览器记住密码弹窗
        prefs = {"": ""}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option("prefs", prefs)
        return options

    def start(self):
        url = 'http://faculty.cau.edu.cn/_wp3services/generalQuery'
        data = {
            "queryObj": "teacherHome",
            # "pageIndex": "1",
            "rows": "52",
            "conditions": '[{"field":"language","value":"1","judge":"="},{"field":"published","value":"1","judge":"="}]',
            "orders": '[{"field":"new","type":"desc"}]',
            "returnInfos": '[{"field":"title","name":"title"},{"field":"cnUrl","name":"cnUrl"},{"field":"post","name":"post"},{"field":"headerPic","name":"headerPic"},{"field":"department","name":"department"},{"field":"exField1","name":"exField1"}]',
            "articleType": "1",
            "level": "0",
            "pageEvent": "doSearchByPage"
        }
        heares = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }
        res = requests.post(url=url, data=data, headers=heares).json()
        print(res)
        nums = res['total']
        print(nums)
        # print(res['data'][806])
        self.driver = webdriver.Chrome(options=self.options())
        self.driver.set_page_load_timeout(5)  # 5秒
        for r in range(0, int(nums)):
            single = res['data'][r]
            print(single)
            name = single['title']
            print(name)
            title = single['post']
            link = single['cnUrl']
            types = single['department']
            if "http://" not in link:
                continue
            try:
                self.driver.get(link)
            except:
                continue
            # 进详情
            time.sleep(0.5)
            photos = self.driver.find_elements(By.XPATH, '//*[@class="fl img_pic" or @class="img_pic"]//img')
            if len(photos) != 0:
                photo = '\n'.join(map(lambda e: e.get_attribute("src"), photos))
            else:
                photo = ''
            counts = self.driver.find_elements(By.XPATH, '//*[@class="inner clearfix"]//li[contains(@class,"item c")]')
            print("有" + str(len(counts)) + "类信息")
            introduce = ''
            if len(counts) != 0:
                for c in counts:
                    c.click()
                    time.sleep(0.5)
                    introduces = self.driver.find_elements(By.XPATH, '//div[contains(@class,"active")]')
                    if len(introduces) != 0:
                        introduces = '\n'.join(map(lambda e: e.text, introduces))
                        introduces = introduces.replace(' ', '')
                        introduce += introduces + '\n\n'
                    else:
                        introduce += ''
            else:
                introduces = self.driver.find_elements(By.XPATH, '//div[contains(@class,"active")]')
                if len(introduces) != 0:
                    introduces = '\n'.join(map(lambda e: e.text, introduces))
                    introduces = introduces.replace(' ', '')
                    introduce += introduces + '\n\n'
                else:
                    introduce += ''
            # print(introduce)
            if "研究领域\n" in introduce:
                field = introduce.split("研究领域\n")[1].split("\n\n")[0]
            else:
                field = ''
            if "联系电话：\n" in introduce:
                phone = introduce.split("联系电话：\n")[1].split("\n")[0]
            else:
                phone = ''
            if "电子邮箱：\n" in introduce:
                mailbox = introduce.split("电子邮箱：\n")[1].split("\n")[0]
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
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./人才-' + self.school + '.xlsx', encoding='xlsxwriter')
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./人才-' + self.school + '.xlsx', encoding='xlsxwriter')
        self.driver.quit()
        print("完成")


if __name__ == '__main__':
    one_url = 'aaa'
    # 学校
    school = '中国农业大学'
    demo = NongyeUniversityNo01(one_url, school)
    demo.start()
