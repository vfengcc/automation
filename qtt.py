import random
import time
import datetime
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

config = {
    "platformName": "Android",
    "platformVersion": "7.1.2",
    "deviceName": "127.0.0.1:62025",
    "udid": "127.0.0.1:62025",
    # "deviceName": "192.168.100.70:4444",
    "appPackage": "com.jifen.qukan",
    "appActivity": "com.jifen.qkbase.main.MainActivity",
    "noReset": True,
    "unicodekeyboard": True,
    "resetkeyboard": True,
    "normalizeTagNames": True,
}

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', config)



def get_size():
    size = driver.get_window_size()
    return size['width'], size['height']


def close_ad(sec=32):
    try:
        if WebDriverWait(driver, 2).until(
                lambda x: x.find_element_by_xpath("//android.widget.RelativeLayout/android.view.View[1]")):
            if WebDriverWait(driver, sec).until(lambda x: x.find_element_by_xpath("//android.widget.TextView[@text='点击重播']")):
                driver.press_keycode(4)  # 返回
                return
    except Exception as e:
        pass

    try:
        if WebDriverWait(driver, 2).until(
                lambda x: x.find_element_by_xpath("//android.view.View[@resource-id='com.jifen.qukan:id/b']")):
            if WebDriverWait(driver, sec).until_not(
                    lambda x: x.find_element_by_xpath("//android.view.View[@resource-id='com.jifen.qukan:id/b']")):
                driver.find_element_by_xpath(
                    "//android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.ImageView[1]").click()
                return
    except Exception as e:
        pass

    # 下载类
    try:
        if WebDriverWait(driver, 2).until(lambda x: x.find_element_by_xpath("//android.widget.TextView[@text='立即下载']")):
            if WebDriverWait(driver, sec).until(
                    lambda x: x.find_element_by_xpath("//android.widget.TextView[@text='点击重播']")):
                driver.press_keycode(4)  # 返回
                return
    except Exception as e:
        pass

    driver.implicitly_wait(sec)
    driver.press_keycode(4)  # 返回
    print('返回')
    # try:
    #     if WebDriverWait(driver, 1).until(lambda x: x.find_element_by_xpath(
    #             "//android.widget.RelativeLayout[@resource-id='com.jifen.qukan:id/tt_video_ad_close_layout']")):
    #         driver.find_element_by_xpath(
    #             "//android.widget.RelativeLayout[@resource-id='com.jifen.qukan:id/tt_video_ad_close_layout']").click()
    #         print('出现关闭框-success，关闭')
    #         return True
    # except Exception as e:
    #     pass
    # driver.press_keycode(4)  # 返回
    # print('返回')


def check_skip():
    ''' 是否有跳过 '''
    try:
        xele = "//android.widget.TextView[@resource-id='com.jifen.qukan:id/o5']"
        if WebDriverWait(driver, 1).until(
                lambda x: x.find_element_by_xpath(xele)):
            driver.find_element_by_xpath(xele).click()
            print('跳过广告：是')
    except Exception as e:
        print('跳过广告： 否')

def check_top_coin():
    ''' 领取成功 '''
    try:
        xele = "//android.widget.TextView[@resource-id='com.jifen.qukan:id/bwp' and @text='领取']"
        if WebDriverWait(driver, 3).until(
                lambda x: x.find_element_by_xpath(xele)):
            driver.find_element_by_xpath(xele).click()
            print('顶部金币： 领取成功')
    except Exception as e:
        print('顶部金币： 无')

def go_to_menu(menu):
    menu_dict = {'头条': 1, '视频': 2, '小视频': 3, '任务': 4, '我的': 5}
    if menu in menu_dict.keys():
        try:
            driver.find_element_by_xpath(
                "//android.widget.LinearLayout[@resource-id='com.jifen.qukan:id/m9']/android.widget.FrameLayout[{}]/android.widget.LinearLayout[1]".format(
                    menu_dict[menu])).click()
        except Exception as e:
            print('go_to_menu - exception')
    time.sleep(3)
    print('进入【{}】页面'.format(menu))

def task_video_coin():
    # 任务-看视频领金币
    time.sleep(2)
    flag = True
    while flag:
        try:
            xele = "//android.support.v7.widget.RecyclerView[@resource-id='com.jifen.qukan:id/bk2']/android.widget.RelativeLayout/android.widget.TextView[@text='看视频领金币']"
            eles = driver.find_elements_by_xpath(xele)
            if len(eles) > 0:
                print('看视频领金币： 有')
                eles[0].click()
                close_ad()
            else:
                flag = False
                print('看视频领金币： 无')
        except Exception as e:
            flag = False
            print('看视频领金币： exception')

def my_yaoqianshu():
    time.sleep(1)
    try:
        if WebDriverWait(driver, 3).until(
                lambda x: x.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.jifen.qukan:id/b8k']")):
            print('进入摇钱树页面 - success')
            driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.jifen.qukan:id/b8k']").click()

            # 剩余次数大于0时，
            try:
                if WebDriverWait(driver, 5).until(
                        lambda x: x.find_element_by_xpath("//android.view.View[@content-desc='领50金币']")):
                    print('页面打开 - 正常')
                    flag = True
                    while flag:
                        try:
                            num_ele = driver.find_element('xpath',
                                                          "//android.webkit.WebView[@content-desc='摇钱树']/android.view.View[1]/android.view.View[4]")
                            num = num_ele.get_attribute('content-desc')
                            if int(num) > 0:
                                driver.find_element('xpath', "//android.view.View[@content-desc='领50金币']").click()
                                close_ad(60)
                                print('摇钱树领金币 - {}次'.format(num))
                            else:
                                print('摇钱树领金币 - 0次')
                                flag = False
                        except Exception as eee:
                            print('摇钱树领金币 - exception', eee)
                            flag = False
                        time.sleep(1)
                else:
                    print('页面打开 - error')
            except Exception as ee:
                print('页面打开 - exception', ee)
        else:
            print('进入摇钱树页面 - error')
    except Exception as e:
        print('进入摇钱树页面 - exception', e)

    time.sleep(2)
    print('摇钱树页面返回')
    driver.press_keycode(4)  # 返回

def small_videos():
    driver.implicitly_wait(3)
    while True:
        looktime = random.randint(10, 15)
        # 阅读奖励
        try:
            if driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.jifen.qukan:id/ay6']"):
                driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.jifen.qukan:id/ay6']").click()
                print('阅读奖励')
                time.sleep(2)
                driver.find_element_by_id("com.jifen.qukan:id/vh").click()
        except Exception as e:
            pass
            # print(111, e)

        # 阅读广告
        try:
            if driver.find_element_by_xpath(
                    "//android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]"):
                looktime = 31
        except Exception as e:
            pass

        print('观看时长：{}s'.format(looktime))
        time.sleep(looktime)

        width, height = get_size()
        x1 = int(width * 0.6)
        y1 = int(height * 0.77)
        y2 = int(height * 0.20)
        driver.swipe(x1, y1, x1, y2)

def tuwen(times=1800):
    ''' 图文 '''
    driver.find_element_by_xpath("//android.widget.LinearLayout[@resource-id='com.jifen.qukan:id/m9']/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]").click()
    print('点击[头条]')
    time.sleep(5)
    # driver.find_element_by_xpath("//android.widget.TextView[@text='推荐']").click()
    # print('点击[推荐]')
    # time.sleep(3)

    def _check_ad(ele):
        try:
            if ele.find_element_by_xpath("android.widget.TextView[@text='广告']"):
                return True
        except Exception as e:
            pass
        return False

    def _check_video(ele):
        try:
            if ele.find_element_by_id("com.jifen.qukan:id/ajk"):
                return True
        except Exception as e:
            pass
        return False

    def _check_ele_exists(ele, node, byt='id'):
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

    def _swipe():
        ''' 滑动 '''
        width, height = get_size()
        x1 = int(width * random.randint(4, 6) / 10)
        x2 = int(width * random.randint(4, 6) / 10)
        y1 = int(height * random.randint(70, 78) / 100)
        y2 = int(height * random.randint(10, 20) / 100)
        driver.swipe(x1, y1, x2, y2)

    def _back():
        ''' 后退 '''
        driver.press_keycode(4)  # 返回

    def tuwen_detail(ele):
        ele.click()
        try:
            if WebDriverWait(driver, 5).until(
                    lambda x: x.find_element_by_id("com.jifen.qukan:id/nf")):
                wait_seconds = random.randint(30, 50)
                while True:
                    if not _check_ele_exists(driver, 'com.jifen.qukan:id/a0q') and not _check_ele_exists(driver, "com.jifen.qukan:id/ay5"):
                        _back()
                        return
                    if _check_ele_exists(driver, "com.jifen.qukan:id/ay5"):
                        driver.find_element_by_id("com.jifen.qukan:id/ay5").click()
                        print('阅读奖励')
                        time.sleep(2)
                        driver.find_element_by_id("com.jifen.qukan:id/vh").click()

                    if _check_ele_exists(driver, "//android.view.View[@text='相关搜索']", "xpath"):
                        print('已到相关推荐 - 返回')
                        _back()
                        return
                    if wait_seconds <= 0:
                        print('达到返回时间 - 返回')
                        _back()
                        return

                    # 2-4s滑屏幕
                    swipe_time = random.randint(1, 3)
                    time.sleep(swipe_time)
                    wait_seconds -= swipe_time

                    ''' 滑动 '''
                    _swipe()
        except Exception as ee:
            print('图文 - 详情 - 异常', ee)
        _back()
        return

    start_stamp = int(datetime.datetime.now().timestamp())
    while True:
        eles = []
        try:
            eles1 = driver.find_elements_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.jifen.qukan:id/l1']/android.widget.LinearLayout")
            eles.extend(eles1)
        except Exception as e:
            pass
        try:
            eles2 = driver.find_elements_by_xpath("//android.support.v7.widget.RecyclerView[@resource-id='com.jifen.qukan:id/l1']/android.widget.RelativeLayout")
            eles.extend(eles2)
        except Exception as e:
            pass
        for ele in eles:
            # 过滤
            is_ad = _check_ad(ele)
            is_video = _check_video(ele)
            if is_ad or is_video:
                print('图文 - 列表 - 过滤')
                continue
            # 获取新闻标题，点击进入详情页面
            try:
                title = str(ele.find_element_by_id("com.jifen.qukan:id/aj3").text).strip()
                tv_from = str(ele.find_element_by_id("com.jifen.qukan:id/am6").text).strip()
                print(title, tv_from)
                # 点击进入详情
                tuwen_detail(ele)

            except Exception as ee:
                print("图文 - 列表 - 缺少元素", ee)
                # pass

            time.sleep(2)
        else:
            print('empty')

        # 判断任务是否完成
        cur_stamp = int(datetime.datetime.now().timestamp())
        if start_stamp + times < cur_stamp:
            print('任务完成')
            _back()
            break

        # 滑动
        _swipe()

check_skip()
check_top_coin()

# go_to_menu('任务')
# task_video_coin()
#
# go_to_menu('我的')
# my_yaoqianshu()
# #
# go_to_menu('小视频')
tuwen(1800)
small_videos()
