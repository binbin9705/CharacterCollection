import pandas as pd, time, requests, json
from selenium import webdriver



class MatchSearch(object):
    def __init__(self, one_url, INVname):
        self.one_url = one_url
        self.INVname = INVname
        # 表头
        self.title = ['0级节点', '1级', '1级行业', '2级', '2级行业','3级', '3级行业']
        self.newList = []  # 0级节点企业数组
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

    def send_token(self):
        url = 'http://39.106.134.50:9528/api/user/login.do'
        datas = {
            "key": "d7XoU6RDTxpO7yuORcQ1+Oxz1SBEyllwGOfme8CSXOJ8IwCsMaONkSaJXd+C870cnPRlNMV5Pc8z+JtBS6ffOatYvC2CiOhebT/n7Xt6zW35HvsQK0hpdkQV/wBA3pNLY9j6TjoYRapTUxf9I6D3a1mZJ0+/+ewST8fm7AqlWZI="}
        res = requests.post(url=url, json=datas).json()
        # print(res)
        # print(res['data'])
        # print(res['data']['token'])
        token = res['data']['token']
        return token

    def start(self):
        # 读取csv
        df = pd.read_csv('newname.csv')
        self.newList = df['INV'].to_numpy()
        print(len(self.newList))
        # 用总行数做循环
        # for c in range(0, int(len(self.newList))):

        for c in range(0,15):
            print("第----------"+str(c)+'--------------行-------')
        # for c in range(0, 1):
            datas = {
                "keyword": str(self.newList[c]),
                "level": "1",
                "attIds": "R101"
                # "attIds": "R102;R101"
            }
            heares = {
                'Token': self.send_token()
            }
            # print(datas)
            # print(heares)
            # print('1级=='+str(res))
            try:
                res = requests.post(url=self.one_url, json=datas, headers=heares).json()
                print(res)
                print("1级" + str(len(res['data']['RESULTDATA']['NODES'])) + '家')
                if int(len(res['data']['RESULTDATA']['NODES'])) <= 1:
                    data = {}
                    data['0级节点'] = self.newList[c]
                    data['1级'] = None
                    data['1级行业'] = None
                    data['2级'] = None
                    data['2级行业'] = None
                    data['3级'] = None
                    data['3级行业'] = None
                    print(data)
                    self.ResultList.append(data)
                else:
                    for s in range(1, int(len(res['data']['RESULTDATA']['NODES']))):
                    # for s in range(0, 3):
                        # 控股企业名称-1级
                        name = res["data"]["RESULTDATA"]["NODES"][s]["NAME"]
                        # 控股企业行业
                        DL_MC = res["data"]["RESULTDATA"]["NODES"][s]["ATTIBUTEMAP"]["DL_MC"]
                        # print(name)
                        # print(DL_MC)
                        # data = {}
                        # data['0级节点'] = self.newList[c]
                        # data['1级'] = name
                        # data['1级行业'] = DL_MC
                        jsondata={
                            "keyword": str(name),
                            "level": "1",
                            # "attIds": "R102;R101"
                            "attIds": "R101"
                        }
                        res2=requests.post(url=self.one_url, json=jsondata, headers=heares).json()
                        print(res2)
                        print('2级'+str(len(res2["data"]["RESULTDATA"]["NODES"]))+'家')
                        # print('2级=='+str(res2))

                        if int(len(res2['data']['RESULTDATA']['NODES'])) <= 1:
                            data = {}
                            data['0级节点'] = self.newList[c]
                            data['1级'] = name
                            data['1级行业'] = DL_MC
                            data['2级'] = None
                            data['2级行业'] = None
                            data['3级'] = None
                            data['3级行业'] = None
                            print(data)
                            self.ResultList.append(data)
                        else:
                            for ss in range(1, int(len(res2['data']['RESULTDATA']['NODES']))):
                                #控股企业-2级
                                name2=res2["data"]["RESULTDATA"]["NODES"][ss]["NAME"]
                                # 控股企业行业
                                DL_MC2 = res2["data"]["RESULTDATA"]["NODES"][ss]["ATTIBUTEMAP"]["DL_MC"]
                                # data['2级'] = name2
                                # data['2级行业'] = DL_MC2
                                jsondata3 = {
                                    "keyword": str(name2),
                                    "level": "1",
                                    # "attIds": "R102;R101"
                                    "attIds": "R101"
                                }
                                res3 = requests.post(url=self.one_url, json=jsondata3, headers=heares).json()
                                print('3级'+ str(len(res3["data"]["RESULTDATA"]["NODES"])) + '家')
                                print(res3)
                                # print('3级==' + str(res3))
                                if int(len(res3['data']['RESULTDATA']['NODES']))<=1:
                                    data = {}
                                    data['0级节点'] = self.newList[c]
                                    data['1级'] = name
                                    data['1级行业'] = DL_MC
                                    data['2级'] = name2
                                    data['2级行业'] = DL_MC2
                                    data['3级'] = None
                                    data['3级行业'] = None
                                    print(data)
                                    self.ResultList.append(data)
                                else:
                                    for sss in range(1, int(len(res3['data']['RESULTDATA']['NODES']))):
                                    # for sss in range(1, 3):
                                        # 控股企业-3级
                                        name3 = res3["data"]["RESULTDATA"]["NODES"][sss]["NAME"]
                                        # 控股企业行业
                                        DL_MC3 = res3["data"]["RESULTDATA"]["NODES"][sss]["ATTIBUTEMAP"]["DL_MC"]
                                        data = {}
                                        data['0级节点'] = self.newList[c]
                                        data['1级'] = name
                                        data['1级行业'] = DL_MC
                                        data['2级'] = name2
                                        data['2级行业'] = DL_MC2
                                        data['3级'] = name3
                                        data['3级行业'] = DL_MC3
                                        print(data)
                                        self.ResultList.append(data)

                                df = pd.DataFrame(self.ResultList, columns=self.title)
                                df.to_excel('./表2-' + '.xlsx')
                                print(self.ResultList)
            except KeyError:
                print("数据未返回跳过这一家")
                break
        print(self.ResultList)
        df = pd.DataFrame(self.ResultList, columns=self.title)
        df.to_excel('./表2-' + '.xlsx')
        print("完成")


if __name__ == '__main__':
    # 在职教师
    one_url = 'http://39.106.134.50:9528/api/interfaceTransfer/transferInter?name=getGraphGCoreData&type=post&id=77C37CD864465584E055000000000001'
    # 学校
    INVname = '无用'
    demo = MatchSearch(one_url, INVname)
    demo.start()

