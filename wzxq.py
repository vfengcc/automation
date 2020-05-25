'''
    玩赚星球
'''
import random
import time
import datetime
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class Wzxq:
    def __init__(self):
        desired_cap = {
            "platformName": "Android",
            # "platformVersion": "7.1.1",
            # "deviceName": '192.168.100.70:4444',
            # "udid": '192.168.100.70:4444',
            "platformVersion": "7.1.2",
            "deviceName": "127.0.0.1:62025",
            "udid": "127.0.0.1:62025",

            "appPackage": "com.planet.light2345",
            "appActivity": "com.planet.light2345.launch.LaunchActivity",
            "noReset": True,
            "unicodekeyboard": True,
            "resetkeyboard": True,
            "normalizeTagNames": True,
        }
        try:
            self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_cap)
        except Exception as e:
            raise ConnectionError('连接错误')

    def _get_size(self):
        ''' 获取宽度+高度 '''
        size = self.driver.get_window_size()
        return size['width'], size['height']

    def _swipe(self):
        ''' 滑动 '''
        width, height = self._get_size()
        x1 = int(width * random.randint(4, 6) / 10)
        x2 = int(width * random.randint(4, 6) / 10)
        y1 = int(height * random.randint(70, 78) / 100)
        y2 = int(height * random.randint(10, 20) / 100)
        self.driver.swipe(x1, y1, x2, y2)

    def _back(self):
        ''' 后退 '''
        self.driver.press_keycode(4)  # 返回

    def _check_ele_exists(self, ele, node, byt='id'):
        ''' 判断节点是否存在 '''
        try:
            ele_sub = None
            if byt == 'id':
                ele_sub = ele.find_element_by_id(node)
            elif byt == 'xpath':
                ele_sub = ele.find_element_by_xpath(node)
            if ele_sub:
                # print('判断节点{} 存在'.format(node))
                return True
            # else:
            #     print('判断节点{} 不存在'.format(node))
        except Exception as e:
            pass
            # print('判断节点{} exception'.format(node), e)
        return False

    def skip_ad(self):
        ''' 跳过广告 '''
        try:
            if WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_id("com.planet.light2345:id/tv_skip")):
                print('跳过广告 - ok')
                self.driver.find_element_by_id("com.planet.light2345:id/tv_skip").click()
        except Exception as e:
            print('跳过广告 - exception')

    def load_index(self):
        ''' 首页加载完成后再继续 '''
        try:
            if WebDriverWait(self.driver, 10).until(
                    lambda x: x.find_element_by_id("com.planet.light2345:id/bottom_tab_layout")):
                print('首页加载 - ok')
                return True
        except Exception as e:
            print('首页加载 - exception')
        return False

    def switch_menu(self, index):
        ''' 切换底部菜单 '''
        self.driver.find_element_by_xpath(
            "//android.widget.LinearLayout[@resource-id='com.planet.light2345:id/bottom_tab_layout']/android.view.ViewGroup[" + str(
                index) + "]/android.widget.ImageView[1]").click()
        print('切换底部菜单-{}'.format(index))
        time.sleep(3)

    def _check_ad(self, ele):
        ''' 判断是否为广告 '''
        try:
            if ele.find_element_by_id("com.startnews.plugin:id/tv_news_tag").text == '广告':
                return True
        except Exception as e:
            pass
        return False

    def tuwen_detail(self, ele):
        ele.click()
        try:
            if WebDriverWait(self.driver, 5).until(
                    lambda x: x.find_element_by_id("com.startnews.plugin:id/img_red_pack")):
                wait_seconds = random.randint(30, 50)
                while True:
                    if self._check_ele_exists(self.driver, "//android.view.View[@content-desc='点击阅读全文']", 'xpath'):
                        self.driver.find_element_by_xpath(
                            "//android.view.View[@content-desc='点击阅读全文']").click()
                    if self._check_ele_exists(self.driver, "//android.view.View[@content-desc='相关推荐']", "xpath"):
                        print('已到相关推荐 - 返回')
                        self._back()
                        return
                    if wait_seconds <= 0:
                        print('达到返回时间 - 返回')
                        self._back()
                        return

                    # 2-4s滑屏幕
                    swipe_time = random.randint(1, 3)
                    time.sleep(swipe_time)
                    wait_seconds -= swipe_time
                    self._swipe()
        except Exception as ee:
            print('图文 - 详情 - 异常', ee)
        self._back()
        return

    def tuwen(self, times=1800):
        ''' 图文 '''
        self.driver.find_element_by_xpath("//android.widget.TextView[@text='推荐']").click()
        time.sleep(3)
        start_stamp = int(datetime.datetime.now().timestamp())
        while True:
            try:
                for ele in self.driver.find_elements_by_xpath(
                        "//android.support.v7.widget.RecyclerView[@resource-id='com.startnews.plugin:id/recycler_news']/android.widget.LinearLayout"):
                    # 过滤
                    is_ad = self._check_ad(ele)
                    is_video = self._check_ele_exists(ele, "com.startnews.plugin:id/img_play")
                    is_recycler_module = self._check_ele_exists(ele, "com.startnews.plugin:id/recycler_news_module")
                    is_health_top = self._check_ele_exists(ele, "com.startnews.plugin:id/rv_health_top")
                    if is_health_top or is_recycler_module or is_ad or is_video:
                        # print('图文 - 列表 - 过滤')
                        continue
                    # 获取新闻标题，点击进入详情页面
                    try:
                        title = str(ele.find_element_by_id("com.startnews.plugin:id/tv_news_title").text).strip()
                        tv_from = str(ele.find_element_by_id("com.startnews.plugin:id/tv_news_from").text).strip()
                        print(title, tv_from)
                        # 点击进入详情
                        self.tuwen_detail(ele)

                    except Exception as ee:
                        # print("图文 - 列表 - 缺少元素", ee)
                        pass
            except Exception as e:
                # print('图文 - 列表 - exception', e)
                pass

            # 判断任务是否完成
            cur_stamp = int(datetime.datetime.now().timestamp())
            if start_stamp + times < cur_stamp:
                print('任务完成')
                self._back()
                break

            # 滑动
            self._swipe()

    def small_videos(self, times=1800):
        ''' 小视频 '''
        self.driver.find_element_by_xpath("//android.widget.TextView[@text='小视频']").click()
        time.sleep(3)
        # 进入详情
        flag = False
        try:
            for ele in self.driver.find_elements_by_xpath(
                    "//android.support.v7.widget.RecyclerView[@resource-id='com.startnews.plugin:id/recycler_news']/android.widget.RelativeLayout"):
                try:
                    if ele.find_element_by_id("com.startnews.plugin:id/small_video_play_count_tv"):
                        ele.click()
                        print('小视频 - 进入详情页')
                        flag = True
                        break
                except Exception as e:
                    pass
        except Exception as e:
            pass

        if flag:
            abletimes = times
            while abletimes > 0:
                # 阅读
                looktime = random.randint(10, 20)
                time.sleep(looktime)
                abletimes -= looktime
                # 滑动
                width, height = self._get_size()
                x1 = int(width * random.randint(4, 6) / 10)
                x2 = int(width * random.randint(4, 6) / 10)
                y1 = int(height * random.randint(65, 72) / 100)
                y2 = int(height * random.randint(30, 35) / 100)
                print("小视频 - 观看时长：{}s 剩余 {}s 坐标：x1-{},y1-{},x2-{},y2-{}".format(looktime, abletimes, x1, y1, x2, y2))
                self.driver.swipe(x1, y1, x2, y2)

            else:
                print("小视频 - 完成任务")
                self._back()  # 返回
        else:
            print("小视频 - 首屏未找到符合的视频")

    def get_top_coin(self):
        ''' 顶部金币 '''
        try:
            if self.driver.find_element_by_id("com.planet.light2345:id/tv_reward_receive_time").text == "领取":
                self.driver.find_element_by_id("com.planet.light2345:id/tv_reward_receive_time").click()
                time.sleep(2)
                self.driver.press_keycode(4)  # 返回
                print('顶部金币 - 领取成功')
        except Exception as e:
            pass


if __name__ == '__main__':
    wzxq = Wzxq()
    wzxq.skip_ad()
    wzxq.load_index()
    wzxq.get_top_coin()
    wzxq.switch_menu(2)
    wzxq.small_videos(1800)
    wzxq.tuwen(300)
