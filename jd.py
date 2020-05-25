import time
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from pymongo import MongoClient
from pymongo.collection import Collection
from concurrent.futures import ThreadPoolExecutor


class Connect_mongo:
    CONFIG_HOST = '127.0.0.1'
    CONFIG_PORT = 27017
    CONFIG_DB = 'jingdong'
    CONFIG_COLLECTION = 'products'
    def __init__(self):
        self.client = MongoClient(host=self.CONFIG_HOST, port=self.CONFIG_PORT)
        self.db_data = self.client[self.CONFIG_DB]
        self.db_collectiopn = Collection(self.db_data, self.CONFIG_COLLECTION)

    def insert_item(self, item):
        self.db_collectiopn.insert_one(item)

class Jd:
    def __init__(self, deviceName, hubUrl):
        desired_cap = {
            "platformName": "Android",
            "platformVersion": "7.1.1",
            "deviceName": deviceName,
            "udid": deviceName,
            "appPackage": "com.jingdong.app.mall",
            "appActivity": "com.jingdong.app.mall.main.MainActivity",
            "noReset": True,
            "unicodekeyboard": True,
            "resetkeyboard": True,
            "normalizeTagNames": True,
        }
        try:
            self.driver = webdriver.Remote(hubUrl, desired_cap)
        except Exception as e:
            raise ConnectionError('连接错误')

        self.device = deviceName
        self.mongo_info = Connect_mongo()

    def _get_size(self):
        ''' 获取宽度+高度 '''
        size = self.driver.get_window_size()
        return size['width'], size['height']

    def search(self, keyword):
        print('首页')
        time.sleep(3)
        try:
            # 如果出现搜索框
            if WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_xpath(
                    "//android.widget.ViewFlipper[1]/android.widget.LinearLayout[1]/android.widget.TextView[1]")):
                print('点击搜索框')
                self.driver.find_element_by_xpath(
                    "//android.widget.ViewFlipper[1]/android.widget.LinearLayout[1]/android.widget.TextView[1]").click()
                time.sleep(3)
                print('输入搜索关键词')
                self.driver.find_element_by_xpath(
                    "//android.widget.EditText[@resource-id='com.jd.lib.search:id/a4c']").send_keys(keyword)
                time.sleep(1)
                print('点击搜索')
                self.driver.find_element_by_xpath(
                    "//android.widget.TextView[@resource-id='com.jingdong.app.mall:id/a9b']").click()
                time.sleep(3)
                titles = []
                try:
                    # 等待出现搜索结果
                    if WebDriverWait(self.driver, 5).until(lambda x: x.find_element_by_id("com.jd.lib.search:id/a55")):
                        flag = True
                        while flag:
                            eles = self.driver.find_elements_by_xpath(
                                "//android.widget.RelativeLayout[@resource-id='com.jd.lib.search:id/a3s']")
                            for ele in eles:
                                try:
                                    item = {}
                                    item['keyword'] = keyword
                                    item['title'] = ele.find_element_by_id("com.jd.lib.search:id/a3u").text
                                    item['price'] = str(
                                        ele.find_element_by_id("com.jd.lib.search:id/abg").text).replace('¥', '')
                                    item['comments'] = ele.find_element_by_id("com.jd.lib.search:id/abj").text
                                    item['comments_good'] = ele.find_element_by_id("com.jd.lib.search:id/abk").text
                                    item['sale'] = ele.find_element_by_id("com.jd.lib.search:id/adz").text

                                    item['is_ad'] = False
                                    try:
                                        if ele.find_element_by_id("com.jd.lib.search:id/a46"):
                                            item['is_ad'] = True
                                    except Exception as eeee:
                                        pass

                                    # 输出 ，存入标题数组， 校验是否已经存在
                                    if item['title'] not in titles:
                                        print(item)
                                        titles.append(item['title'])
                                        # 写入数据库
                                        self.mongo_info.insert_item(item)
                                except Exception as eee:
                                    pass
                                    # print('row - exception', eee)

                            # 判断是否到底
                            try:
                                if self.driver.find_element_by_id("com.jd.lib.search:id/agw"):
                                    flag = False
                                    break
                            except Exception as e1:
                                pass

                            # 滑屏
                            width, height = self._get_size()
                            x = int(width * 0.3)
                            y1 = int(height * 0.8)
                            y2 = int(height * 0.3)
                            self.driver.swipe(x, y1, x, y2)

                except Exception as ee:
                    print('等待搜索结果 - exception', ee)

        except Exception as e:
            print(self.device, e)


def handler(deviceName, hubUrl, keyword):
    jd = Jd(deviceName, hubUrl)
    jd.search(keyword)


if __name__ == '__main__':

    devices_list = [
        {'deviceName': '192.168.100.111:4444', 'hubUrl': 'http://127.0.0.1:4723/wd/hub', 'keyword': '盘珠大米50斤'},
        {'deviceName': '127.0.0.1:62026', 'hubUrl': 'http://127.0.0.1:4725/wd/hub', 'keyword': '山东茄子5斤'}
    ]
    m_list = []

    # 最大20个线程
    pool = ThreadPoolExecutor(max_workers=5)
    for device in devices_list:
        jd = Jd(device['deviceName'], device['hubUrl'])
        pool.submit(jd.search, device['keyword'])

        # m_list.append(multiprocessing.Process(target=jd.search, args=(device['keyword'],)))
    # for m in m_list:
    #     m.start()
    # for m in m_list:
    #     m.join()
