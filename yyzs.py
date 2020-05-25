import random
import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class Yyzs:
    CONFIG = {
        "platformName": "Android",
        "platformVersion": "7.1.2",
        # "platformVersion": "6.0.1",
        "deviceName": "127.0.0.1:62026",
        "udid": "127.0.0.1:62026",
        # "deviceName": "192.168.100.71:4444",
        "appPackage": "com.ll.fishreader",
        "appActivity": "com.ll.fishreader.ui.activity.SplashActivity",
        "noReset": True,
        "unicodekeyboard": True,
        "resetkeyboard": True,
        "normalizeTagNames": True,
    }

    RAND_SLEEP = (15, 25)

    def get_driver(self):
        repet_nums = 5
        while repet_nums > 0:
            try:
                return webdriver.Remote('http://127.0.0.1:4725/wd/hub', self.CONFIG)
            except Exception as e:
                repet_nums -= 1
                print('尝试重连')
        return False

    def __init__(self, times=1800):
        self.driver = self.get_driver()
        if not self.driver:
            print('连接失败')
            raise ValueError('连接失败')
        self.times = times

    def get_size(self):
        size = self.driver.get_window_size()
        return size['width'], size['height']

    def home_to_look(self):
        ''' 首页点击 “继续阅读” '''
        try:
            if WebDriverWait(self.driver, 3).until(
                    lambda x: x.find_element_by_id("com.ll.fishreader:id/recent_book_record_continue_tv")
            ):
                self.driver.find_element_by_id("com.ll.fishreader:id/recent_book_record_continue_tv").click()
        except Exception as e:
            print('无继续阅读')

        while self.times > 0:
            looktime = random.randint(*self.RAND_SLEEP)
            print('时长:{}s'.format(looktime), end='\t')
            time.sleep(looktime)

            width, height = self.get_size()
            x1 = int(width * random.randint(85, 90) / 100)
            x2 = int(width * random.randint(10, 20) / 100)
            y1 = int(height * random.randint(70, 85) / 100)
            y2 = int(height * random.randint(50, 65) / 100)
            print("坐标：x1-{},y1-{},x2-{},y2-{}".format(x1, y1, x2, y2))
            try:
                self.driver.swipe(x1, y1, x2, y2)
            except Exception as e:
                print('swipe - exception', e)
            # print("坐标：x1-{},y1-{},x2-{},y2-{}".format(x1, y1, x2, y2))
            self.times -= looktime

    # def weixin_share(self):
    #     try:
    #         if WebDriverWait(self.driver, 5).until(
    #                 lambda x: x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tencent.mm:id/b2b']")
    #         ):
    #             self.driver.press_keycode(4)  # 返回
    #     except Exception as e:
    #         self.driver.press_keycode(4)  # 返回
    #         print('wx_share - exception', e)
    #


    # def top_coin(self):
    #     ''' 顶部金币 '''
    #     try:
    #         self.driver.find_element_by_id(
    #             "com.ll.fishreader:id/tt_video_ad_close").click()
    #         time.sleep(3)
    #         try:
    #             # 等待
    #             if WebDriverWait(self.driver, 35).until(lambda x: x.find_element_by_id( "com.ll.fishreader:id/tt_video_ad_close")):
    #                 # 点击
    #                 self.driver.find_element_by_id("com.ll.fishreader:id/tt_video_ad_close").click()
    #                 self.pop_close()
    #         except Exception as e:
    #             self.driver.press_keycode(4)  # 返回
    #
    #         print('顶部金币 - 可领取')
    #     except Exception as e:
    #         print('顶部金币 - 不可领取')

    def resetSys(self):
        print('=======开始重启： 长按电源=>点击重启 ========')
        try:
            self.driver.implicitly_wait(30)
            self.driver.long_press_keycode(26)
            time.sleep(3)
            self.driver.find_element_by_xpath(
                "//android.widget.TextView[@resource-id='android:id/message' and @text='重新启动']").click()
        except Exception as e:
            print('重启', e)
        print('=======开始重启： 长按电源=>点击重启 end========')

    def check1(self):
        print('检查start广告')
        try:
            if WebDriverWait(self.driver, 5).until(
                    lambda x: x.find_element_by_id('com.ll.fishreader:id/jump_widget_1')):
                self.driver.find_element_by_id('com.ll.fishreader:id/jump_widget_1').click()
                print('跳过ad')
        except Exception as e:
            pass

    def check2(self):
        print('检查首页 - 弹窗')
        try:
            if WebDriverWait(self.driver, 5).until(
                    lambda x: x.find_element_by_id('com.ll.fishreader:id/jump_widget_1')):
                self.driver.find_element_by_id('com.ll.fishreader:id/widget_image_floatwindow_close').click()
                print('关闭')
        except Exception as e:
            pass

    def check3(self):
        print('检查首页 - 是否加载完')
        try:
            if WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id(
                    "com.ll.fishreader:id/recent_book_record_continue_tv")):
                print('加载完成')
            else:
                print('加载失败')
        except Exception as e:
            print('加载异常', e)

    def pop_close(self):
        print('检查 - 收入囊中 - 关闭')
        try:
            if WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath("//android.widget.Button[@text='收入囊中']")):
                self.driver.find_element_by_xpath("//android.widget.Button[@text='收入囊中']").click()
            else:
                print('加载失败')
        except Exception as e:
            print('加载异常', e)

    def run(self):
        self.check1()
        self.check2()
        self.check3()

        self.home_to_look()

        # self.top_coin()
        # self.home_to_look()
        # self.resetSys()


while True:
    time.sleep(5)
    njxs = Yyzs(3600)
    njxs.run()
    print('结束')
    break
