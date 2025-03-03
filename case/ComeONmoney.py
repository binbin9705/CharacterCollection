import pandas as pd, time, logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from collections import Counter


class ComeONmoney(object):
    def __init__(self, data_url):
        self.data_url = data_url
        # self.two_url = two_url
        # self.three_url = three_url
        # self.four_url = four_url
        # self.school=school
        # 表头
        # self.title = ['万位1','万位2','万位3','万位4','万位5',
        #               '千位1','千位2','千位3','千位4','千位5',
        #               '百位1','百位2','百位3','百位4','百位5',
        #               '十位1','十位2','十位3','十位4','十位5',
        #               '个位1','个位2','个位3','个位4','个位5']
        self.title = ['万位', '千位', '百位', '十位', '个位']
        self.ResultList = []  # 最终数据
        self.wanResultList = []  # 万最终数据
        self.qianResultList = []  # 千最终数据
        self.baiResultList = []  # 百最终数据
        self.shiResultList = []  # 十最终数据
        self.geResultList = []  # 个最终数据
        current_timestamp = time.time()
        # 将时间戳转换为日期格式
        self.current_date = time.strftime('%Y-%m-%d', time.localtime(current_timestamp))

    def options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")  # 规避监测selenium
        options.add_argument('--start-maximized')  # 全屏运行
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 不显示chrome受自动控制提示
        options.add_argument('--disable-extensions')
        # 关掉浏览器记住密码弹窗
        prefs = {"": ""}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option("prefs", prefs)
        # options.headless=True
        return options

    def start(self):
        self.driver = webdriver.Chrome(options=self.options())
        for data_url in self.data_url:
            print(data_url)
            self.driver.get(data_url)
            time.sleep(2)
            element = self.driver.find_elements(By.XPATH, "//div[@class='cm-box m-news-fore']")  # 两个数组
            # print(len(element))
            for x in range(1, len(element) + 1):
                datanum = self.driver.find_elements(By.XPATH, '//div[@class="cm-box m-news-fore"][' + str(x) + ']//a')
                # print(len(datanum))
                for s in range(1, len(datanum) + 1):
                    # print(s)
                    link = self.driver.find_element(By.XPATH,
                                                    '//div[@class="cm-box m-news-fore"][' + str(x) + ']//a[' + str(
                                                        s) + ']').get_attribute('href')
                    # print(link)
                    self.driver.get(link)
                    time.sleep(2)
                    text = self.driver.find_element(By.XPATH, '//table/..').text
                    newtext = text.split("推荐：")[1]
                    print(newtext)
                    wannum = newtext.split("万位定5：")[1].split("千位定5：")[0]
                    wannumlist = wannum.split()
                    wannum = ','.join(wannumlist)
                    qiannum = newtext.split("千位定5：")[1].split("百位定5：")[0]
                    qiannumlist = qiannum.split()
                    qiannum = ','.join(qiannumlist)
                    bainum = newtext.split("百位定5：")[1].split("十位定5：")[0]
                    bainumlist = bainum.split()
                    bainum = ','.join(bainumlist)
                    shinum = newtext.split("十位定5：")[1].split("个位定5：")[0]
                    shinumlist = shinum.split()
                    shinum = ','.join(shinumlist)
                    genum = newtext.split("个位定5：")[1]
                    genumlist = genum.split()
                    genum = ','.join(genumlist)
                    data = {}
                    data['万位'] = wannum
                    data['千位'] = qiannum
                    data['百位'] = shinum
                    data['十位'] = bainum
                    data['个位'] = genum
                    print(data)
                    self.ResultList.append(data)
                    # print(self.ResultList)
                    self.wanResultList.extend(wannumlist)
                    self.qianResultList.extend(qiannumlist)
                    self.baiResultList.extend(bainumlist)
                    self.shiResultList.extend(shinumlist)
                    self.geResultList.extend(genumlist)
                    self.driver.back()
                    df = pd.DataFrame(self.ResultList, columns=self.title)
                    df.to_excel('./' + self.current_date + '参考数据' + '.xlsx')
            df = pd.DataFrame(self.ResultList, columns=self.title)
            df.to_excel('./' + self.current_date + '参考数据' + '.xlsx')
        print(self.ResultList)

        wantwo = Counter(self.wanResultList)
        wantwo = sorted(wantwo.items(), key=lambda item: item[1], reverse=True)
        print(
            f'万位出现最多的前五位数是：{wantwo[0][0]},{wantwo[1][0]},{wantwo[2][0]},{wantwo[3][0]},{wantwo[4][0]}\n{wantwo[0][0]}：{wantwo[0][1]}次\n{wantwo[1][0]}：{wantwo[1][1]}次\n{wantwo[2][0]}：{wantwo[2][1]}次\n{wantwo[3][0]}：{wantwo[3][1]}次\n{wantwo[4][0]}：{wantwo[4][1]}次')

        qiantwo = Counter(self.qianResultList)
        qiantwo = sorted(qiantwo.items(), key=lambda item: item[1], reverse=True)
        print(
            f'千位出现最多的前五位数是：{qiantwo[0][0]},{qiantwo[1][0]},{qiantwo[2][0]},{qiantwo[3][0]},{qiantwo[4][0]}\n{qiantwo[0][0]}：{qiantwo[0][1]}次\n{qiantwo[1][0]}：{qiantwo[1][1]}次\n{qiantwo[2][0]}：{qiantwo[2][1]}次\n{qiantwo[3][0]}：{qiantwo[3][1]}次\n{qiantwo[4][0]}：{qiantwo[4][1]}次')

        baitwo = Counter(self.baiResultList)
        baitwo = sorted(baitwo.items(), key=lambda item: item[1], reverse=True)
        print(
            f'百位出现最多的前五位数是：{baitwo[0][0]},{baitwo[1][0]},{baitwo[2][0]},{baitwo[3][0]},{baitwo[4][0]}\n{baitwo[0][0]}：{baitwo[0][1]}次\n{baitwo[1][0]}：{baitwo[1][1]}次\n{baitwo[2][0]}：{baitwo[2][1]}次\n{baitwo[3][0]}：{baitwo[3][1]}次\n{baitwo[4][0]}：{baitwo[4][1]}次')

        shitwo = Counter(self.shiResultList)
        shitwo = sorted(shitwo.items(), key=lambda item: item[1], reverse=True)
        print(
            f'十位出现最多的前五位数是：{shitwo[0][0]},{shitwo[1][0]},{shitwo[2][0]},{shitwo[3][0]},{shitwo[4][0]}\n{shitwo[0][0]}：{shitwo[0][1]}次\n{shitwo[1][0]}：{shitwo[1][1]}次\n{shitwo[2][0]}：{shitwo[2][1]}次\n{shitwo[3][0]}：{shitwo[3][1]}次\n{shitwo[4][0]}：{shitwo[4][1]}次')

        getwo = Counter(self.geResultList)
        getwo = sorted(getwo.items(), key=lambda item: item[1], reverse=True)
        print(
            f'个位出现最多的前五位数是：{getwo[0][0]},{getwo[1][0]},{getwo[2][0]},{getwo[3][0]},{getwo[4][0]}\n{getwo[0][0]}：{getwo[0][1]}次\n{getwo[1][0]}：{getwo[1][1]}次\n{getwo[2][0]}：{getwo[2][1]}次\n{getwo[3][0]}：{getwo[3][1]}次\n{getwo[4][0]}：{getwo[4][1]}次')
        print(
            f'\n根据统计得出结果'
            f'\n推荐排列5复试各选5:'
            f'\n总计：3125 注\n共需要：3125 * 2 = 6250 元'
            f'\n第一位:{wantwo[0][0]},{wantwo[1][0]},{wantwo[2][0]},{wantwo[3][0]},{wantwo[4][0]}'
            f'\n第二位:{qiantwo[0][0]},{qiantwo[1][0]},{qiantwo[2][0]},{qiantwo[3][0]},{qiantwo[4][0]}'
            f'\n第三位:{baitwo[0][0]},{baitwo[1][0]},{baitwo[2][0]},{baitwo[3][0]},{baitwo[4][0]}'
            f'\n第四位:{shitwo[0][0]},{shitwo[1][0]},{shitwo[2][0]},{shitwo[3][0]},{shitwo[4][0]}'
            f'\n第五位:{getwo[0][0]},{getwo[1][0]},{getwo[2][0]},{getwo[3][0]},{getwo[4][0]}')
        print(
            f'\n推荐排列5复试各选4:'
            f'\n总计：1024 注\n共需要：1024 * 2 = 2048 元'
            f'\n第一位:{wantwo[0][0]},{wantwo[1][0]},{wantwo[2][0]},{wantwo[3][0]}'
            f'\n第二位:{qiantwo[0][0]},{qiantwo[1][0]},{qiantwo[2][0]},{qiantwo[3][0]}'
            f'\n第三位:{baitwo[0][0]},{baitwo[1][0]},{baitwo[2][0]},{baitwo[3][0]}'
            f'\n第四位:{shitwo[0][0]},{shitwo[1][0]},{shitwo[2][0]},{shitwo[3][0]}'
            f'\n第五位:{getwo[0][0]},{getwo[1][0]},{getwo[2][0]},{getwo[3][0]}')

        print(
            f'\n推荐排列5复试各选3:'
            f'\n总计：243 注\n共需要：243 * 2 = 486 元'
            f'\n第一位:{wantwo[0][0]},{wantwo[1][0]},{wantwo[2][0]}'
            f'\n第二位:{qiantwo[0][0]},{qiantwo[1][0]},{qiantwo[2][0]}'
            f'\n第三位:{baitwo[0][0]},{baitwo[1][0]},{baitwo[2][0]}'
            f'\n第四位:{shitwo[0][0]},{shitwo[1][0]},{shitwo[2][0]}'
            f'\n第五位:{getwo[0][0]},{getwo[1][0]},{getwo[2][0]}')

        print(
            f'\n推荐排列5复试各选2:'
            f'\n总计：32 注\n共需要：32 * 2 = 64 元'
            f'\n第一位:{wantwo[0][0]},{wantwo[1][0]}'
            f'\n第二位:{qiantwo[0][0]},{qiantwo[1][0]}'
            f'\n第三位:{baitwo[0][0]},{baitwo[1][0]}'
            f'\n第四位:{shitwo[0][0]},{shitwo[1][0]}'
            f'\n第五位:{getwo[0][0]},{getwo[1][0]}')

        print(
            f'\n推荐排列5 1注:'
            f'\n总计：1 注\n共需要：1 * 2 = 2 元'
            f'\n{wantwo[0][0]} {qiantwo[0][0]} {baitwo[0][0]} {shitwo[0][0]} {getwo[0][0]}')
        print('\n')
        print(
            f'\n推荐排列3复试各选5:'
            f'\n总计：125 注\n共需要：125 * 2 = 250 元'
            f'\n第一位:{wantwo[0][0]},{wantwo[1][0]},{wantwo[2][0]},{wantwo[3][0]},{wantwo[4][0]}'
            f'\n第二位:{qiantwo[0][0]},{qiantwo[1][0]},{qiantwo[2][0]},{qiantwo[3][0]},{qiantwo[4][0]}'
            f'\n第三位:{baitwo[0][0]},{baitwo[1][0]},{baitwo[2][0]},{baitwo[3][0]},{baitwo[4][0]}')
        print(
            f'\n推荐排列3复试各选4:'
            f'\n总计：64 注\n共需要：64 * 2 = 128 元'
            f'\n第一位:{wantwo[0][0]},{wantwo[1][0]},{wantwo[2][0]},{wantwo[3][0]}'
            f'\n第二位:{qiantwo[0][0]},{qiantwo[1][0]},{qiantwo[2][0]},{qiantwo[3][0]}'
            f'\n第三位:{baitwo[0][0]},{baitwo[1][0]},{baitwo[2][0]},{baitwo[3][0]}')
        print(
            f'\n推荐排列3复试各选3:'
            f'\n总计：27 注\n共需要：27 * 2 = 54 元'
            f'\n第一位:{wantwo[0][0]},{wantwo[1][0]},{wantwo[2][0]}'
            f'\n第二位:{qiantwo[0][0]},{qiantwo[1][0]},{qiantwo[2][0]}'
            f'\n第三位:{baitwo[0][0]},{baitwo[1][0]},{baitwo[2][0]}')

        print(
            f'\n推荐排列3复试各选2:'
            f'\n总计：8 注\n共需要：8 * 2 = 16 元'
            f'\n第一位:{wantwo[0][0]},{wantwo[1][0]}'
            f'\n第二位:{qiantwo[0][0]},{qiantwo[1][0]}'
            f'\n第三位:{baitwo[0][0]},{baitwo[1][0]}')
        print(
            f'\n推荐排列3 1注:'
            f'\n总计：1 注\n共需要：1 * 2 = 2 元'
            f'\n{wantwo[0][0]} {qiantwo[0][0]} {baitwo[0][0]}')

        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./' + self.current_date + '参考数据' + '.xlsx')
        self.driver.quit()
        print("理性购彩,量力而行\n祝君中奖")

if __name__ == '__main__':
    # data_url = 'https://www.yiqicai.com/pl5/yc/'
    # data_url = 'https://www.yiqicai.com/pl5/yc/1'
    # data_url = 'https://www.yiqicai.com/pl5/yc/2'
    data_url = ['https://www.yiqicai.com/pl5/yc/', 'https://www.yiqicai.com/pl5/yc/1',
                'https://www.yiqicai.com/pl5/yc/2']
    demo = ComeONmoney(data_url)
    demo.start()
