import pandas as pd, time, logging, colorlog,requests,json,re ,glob,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class DEMO(object):
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


    def start(self):
        # 定义文件夹路径
        folder_path = './'
        # 获取文件夹下所有的Excel文件
        excel_files = glob.glob(os.path.join(folder_path, '*.xlsx')) + glob.glob(os.path.join(folder_path, '*.xls'))+ glob.glob(os.path.join(folder_path, '*.csv'))
        # 遍历Excel文件并修改文件名
        for file_path in excel_files:
            # 获取文件名和扩展名
            file_dir, file_name = os.path.split(file_path)
            file_base_name, file_ext = os.path.splitext(file_name)
            print("1:"+file_dir)
            print("2:"+file_name)
            print("3:"+file_base_name)
            print("4:"+file_ext)
            # print(file_base_name[:-2])
            file_base_name=file_base_name[:-1]
            # 这里可以根据需要修改文件名的逻辑
            new_file_name = file_base_name + '7' + file_ext
            # 构建新的文件路径
            new_file_path = os.path.join(file_dir, new_file_name)
            # 重命名文件
            os.rename(file_path, new_file_path)


if __name__ == '__main__':
    one_url = 'https://www.beijing.gov.cn/ywdt/zwzt/jjjyth/xy/'
    # 学校
    school = '京津冀-三地协议'
    demo = DEMO(one_url, school)
    demo.start()
