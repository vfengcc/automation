import sys
import time
import hashlib
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class Pdd:
    def __init__(self):
        desired_caps = {
            "platformName": "Android",
            # "platformVersion": "7.1.1",
            "platformVersion": "6.0.1",
            # "deviceName": "192.168.100.111:4444",
            "deviceName": "192.168.100.71:4444",
            "appPackage": "com.xunmeng.pinduoduo",
            # "appActivity": "com.xunmeng.pinduoduo/com.xunmeng.pinduoduo.ui.activity.HomeActivity",
            # "appActivity": "com.xunmeng.pinduoduo.ui.activity.OriginLogoActivity",
            "appActivity": "com.xunmeng.pinduoduo.ui.activity.MainFrameActivity",
            # "waitappActivity": "com.xunmeng.pinduoduo.ui.activity.MainFrameActivity",
            "noReset": True,
            # 隐藏键盘
            # 'unicodeKeyboard': True,
            # 'resetKeyboard': True,
        }
        repet_nums = 5
        while repet_nums > 0:
            try:
                self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
                print('连接成功')
                break
            except Exception as e:
                repet_nums -= 1
                print('尝试重连', e)
        else:
            raise ConnectionError('连接错误')

    def get_size(self):
        size = self.driver.get_window_size()
        return size['width'], size['height']

    def switch_menu(self, menu):
        ''' 切换底部菜单 '''
        menus = {'首页': 1, '关注': 2, '分类': 3, '聊天': 4, '个人中心': 5}
        if menu in menus.keys():
            try:
                self.driver.find_element_by_xpath(
                    "//android.widget.TextView[@text='{}']".format(menu)).click()
            except Exception as e:
                print(menu + '点击 - exception ', e)

            print('进入-{}'.format(menu))
            time.sleep(3)
        else:
            print('未定义的menu')

    def goto_index_button(self, button):
        ''' 首页 中间部位 按钮 '''
        buttons = ['多多赚大钱', '限时秒杀']
        if button in buttons:
            self.driver.find_element_by_xpath("//android.widget.TextView[@text='多多赚大钱']")
            print('进入-{}'.format(button))
            time.sleep(3)
        else:
            print('未定义的menu')

    def myorder(self):
        # try:
        if WebDriverWait(self.driver, 3).until(
                lambda x: x.find_element_by_xpath("//android.widget.TextView[@text='查看全部']")):
            self.driver.find_element_by_xpath("//android.widget.TextView[@text='查看全部']").click()
            print('进入我的订单')
            time.sleep(3)
            listarea_1 = self.driver.find_elements_by_xpath(
                "//android.support.v7.widget.RecyclerView[@resource-id='com.xunmeng.pinduoduo:id/c32']/android.widget.LinearLayout")
            print(listarea_1)
            for ele in listarea_1:
                if ele.find_element_by_id("com.xunmeng.pinduoduo:id/deq"):
                    item = {}
                    item['sale'] = ele.find_element_by_id("com.xunmeng.pinduoduo:id/deq").text
                    item['status'] = ele.find_element_by_id("com.xunmeng.pinduoduo:id/di9").text
                    item['title'] = ele.find_element_by_id("com.xunmeng.pinduoduo:id/d_u").text
                    item['price'] = str(ele.find_element_by_id("com.xunmeng.pinduoduo:id/da2").text).replace(
                        '¥', '')
                    item['number'] = str(ele.find_element_by_id("com.xunmeng.pinduoduo:id/d24").text).replace(
                        '×', '')
                    item['guige'] = str(ele.find_element_by_id("com.xunmeng.pinduoduo:id/d_a").text).replace(
                        '×', '')
                    item['paid'] = str(ele.find_element_by_id("com.xunmeng.pinduoduo:id/cxd").text)
                    item['tran'] = str(ele.find_element_by_id("com.xunmeng.pinduoduo:id/d9h").text)

                    # 点击进入详情页面
                    print(item)
                    try:
                        ele.find_element_by_id("com.xunmeng.pinduoduo:id/d_u").click()
                        print('点击订单详情 - ok')
                    except Exception as e:
                        print('点击订单详情 - exception', e)

                    time.sleep(3)
                    print('--------test详情元素-----------')
                    try:
                        print('aaaaa=====')
                        print(self.driver.find_element_by_xpath(
                            # "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/com.tencent.tbs.core.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.widget.ListView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]"))
                            "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/com.tencent.tbs.core.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[4]"))
                    except Exception as e:
                        print('aaaaa',e)

                    try:
                        print('bbbbb=======')
                        print(self.driver.find_element_by_id("TYVaoW2I"))
                    except Exception as e:
                        print('bbbbb',e)
                    try:
                        print('bbbbbbbbbb')
                        print(self.driver.find_element_by_xpath(
                            # "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/com.tencent.tbs.core.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.widget.ListView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]"))
                            "//com.tencent.tbs.core.webkit.WebView/android.webkit.WebView[@text='拼多多']/android.view.View[0]"))
                    except Exception as e:
                        print('bbbbb',e)
                    try:
                        print('cccccccc')
                        print(self.driver.find_element_by_xpath(
                            # "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/com.tencent.tbs.core.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.widget.ListView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]"))
                            "//com.tencent.tbs.core.webkit.WebView/android.webkit.WebView[@text='拼多多']/android.view.View[1]/android.widget.ListView[5]"))
                    except Exception as e:
                        print('cccccc',e)
                    print('-------------')
                    self.driver.press_keycode(4)  # 返回
                    print('返回')

                # try:
                #
                #
                # except Exception as e:
                #     print(e)


            # flag = True
            # while flag:
            #     listarea_1 = self.driver.find_elements_by_xpath(
            #         "//android.support.v7.widget.RecyclerView[@resource-id='com.xunmeng.pinduoduo:id/c2g']/android.widget.LinearLayout")
            #     for ele in listarea_1:
            #         try:
            #             if ele.find_element_by_id("com.xunmeng.pinduoduo:id/ddz"):
            #                 item = {}
            #                 item['sale'] = ele.find_element_by_id("com.xunmeng.pinduoduo:id/ddz").text
            #                 item['status'] = ele.find_element_by_id("com.xunmeng.pinduoduo:id/dhh").text
            #                 item['title'] = ele.find_element_by_id("com.xunmeng.pinduoduo:id/d_4").text
            #                 item['price'] = str(ele.find_element_by_id("com.xunmeng.pinduoduo:id/d_b").text).replace(
            #                     '¥', '')
            #                 item['number'] = str(ele.find_element_by_id("com.xunmeng.pinduoduo:id/d1g").text).replace(
            #                     '×', '')
            #                 item['guige'] = str(ele.find_element_by_id("com.xunmeng.pinduoduo:id/d9k").text).replace(
            #                     '×', '')
            #                 item['paid'] = str(ele.find_element_by_id("com.xunmeng.pinduoduo:id/cwq").text)
            #                 item['tran'] = str(ele.find_element_by_id("com.xunmeng.pinduoduo:id/d8r").text)
            #
            #                 # 点击进入详情页面
            #                 print(item)
            #                 ele.find_element_by_id("com.xunmeng.pinduoduo:id/d_4").click()
            #                 time.sleep(1)
            #                 print(self.driver.find_element_by_xpath(
            #                     "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/com.tencent.tbs.core.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.widget.ListView[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]").text)
            #
            #                 sys.exit(1)
            #         except Exception as e:
            #             pass
            #
            #     # 判断是否达到最低端
            #     try:
            #         if self.driver.find_element_by_xpath("//android.widget.TextView[@text='没找到订单？试试查看全部或更换登录方式']"):
            #             print('没数据了')
            #             flag = False
            #             break
            #     except Exception as e:
            #         pass
            #
            #     # 处理滑动
            #     width, height = self.get_size()
            #     x = int(width * 0.3)
            #     y1 = int(height * 0.8)
            #     y2 = int(height * 0.3)
            #     print('滑动')
            #     self.driver.swipe(x, y1, x, y2)
            #
            #     # 停顿
            #     time.sleep(2)

    def get_order_detail(self, ele):
        ele.click()
        time.sleep(1)



        # except Exception as e:
        #     print('进入【我的订单】- exception', e)

    def zdq(self):
        self.goto_index_button('多多赚大钱')
        try:
            if WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_xpath(
                    "//android.widget.ViewSwitcher[@resource-id='com.xunmeng.pinduoduo:id/crn']")):
                self.driver.press_keycode(4)  # 返回
        except Exception as e:
            pass


if __name__ == '__main__':
    pdd = Pdd()
    time.sleep(10)
    pdd.switch_menu('个人中心')
    pdd.myorder()
