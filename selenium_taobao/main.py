import logging
import json
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyquery import PyQuery as pq

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


class Taobao:
    COOKIE_FILE = 'cookies_taobao.json'

    def __init__(self, tuser, tpwd='', drivertype='chrome', droverpath='drivers/chromedriver.exe'):
        self.index_handle = None
        if drivertype == 'chrome':
            option = webdriver.ChromeOptions()
            # option.add_argument('--headless')  # 不提供可视化页面
            option.add_argument('--no-sandbox')
            option.add_argument('--disable-dev-shm-usage')
            option.add_argument("--window-size=1920,1080")
            option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
            self.browser = webdriver.Chrome(executable_path=droverpath, options=option)
        self.wait = WebDriverWait(self.browser, 15)
        self.username = tuser
        self.password = tpwd

        self.index()  # 打开淘宝首页

    def index(self):
        ''' 打开淘宝首页 - 加载cookie - 校验cookie - 登录'''
        self.browser.get('https://www.taobao.com/')
        time.sleep(random.randint(3, 7))
        self.check_cookie()  # 检查cookie是否可用

        nickname_ele = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.member-nick')))
        nickname = nickname_ele.text.strip()
        if nickname == '你好':
            time.sleep(random.randint(5, 15))
            self.login()
            nickname_ele = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.member-nick')))
            nickname = nickname_ele.text.strip()
        if nickname and nickname != '你好':
            logging.info('【{}】登录成功'.format(nickname))
        else:
            raise RuntimeError('登录失败，无法进行后续操作，中止')

    def login(self):
        '''登录操作'''
        self.index_handle = self.browser.current_window_handle
        member_areas = self.browser.find_elements_by_css_selector('.J_MemberLogout >a')
        for member in member_areas:
            if member.text == '登录':
                logging.info('点击登录按钮，进入登录页面')
                time.sleep(random.randint(3, 10))
                handles_org = self.browser.window_handles  # 记录点击前的窗口 登录页面为新打开的标签页，所以需要下面多了一堆操作
                member.click()  # 点击登录
                logging.info('新标签 - 打开登录页面')
                time.sleep(random.randint(3, 13))
                handles_new = self.browser.window_handles
                handle = [hand for hand in handles_new if hand not in handles_org]
                self.browser.close()
                self.browser.switch_to.window(handle[0])

                logging.info('模拟登陆')
                user_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#fm-login-id')))
                pwd_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#fm-login-password')))
                login_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password-login')))

                user_input.send_keys(self.username)
                time.sleep(random.randint(3, 8))
                pwd_input.send_keys(self.password)
                time.sleep(random.randint(5, 10))
                try:
                    slide = self.browser.find_element_by_id('nc_1_n1z')
                    if slide:
                        webdriver.ActionChains(self.browser).drag_and_drop_by_offset(slide, 280, 0).perform()
                        time.sleep(random.randint(4, 7))
                except Exception as e:
                    pass

                login_btn.click()
                time.sleep(random.randint(15, 20))
                if str(self.browser.current_url).find('login.taobao.com') == -1:
                    logging.info('登录成功， 存储cookie')
                    self.set_cookie(self.browser.get_cookies())
                break
        else:
            logging.error('登录按钮未找到')

    def check_cookie(self):
        '''检查cookie, 异常则删除all_cookie,返回首页重新登录'''
        fcookie = self.get_cookie()
        if fcookie:
            original_window = self.browser.current_window_handle
            logging.info('加载cookie')
            self.add_cookie_to_options(fcookie)
            logging.info('ctrl + t 开启新tab')

            handles_org = self.browser.window_handles
            # self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL, "t")
            self.browser.execute_script('window.open()')
            # time.sleep(random.randint(3, 5))
            handles_new = self.browser.window_handles
            handle = [hand for hand in handles_new if hand not in handles_org]
            self.browser.switch_to.window(handle[0])

            logging.info('打开"我的淘宝"页面')
            self.browser.get('https://trade.taobao.com/trade/itemlist/list_bought_items.htm')
            time.sleep(random.randint(3, 8))
            if self.browser.current_url.find('login.taobao.com') != -1:
                logging.info('url出现登录域名，删除cookie')
                logging.info('需要登录')
                logging.info('del-cookie')
                self.browser.delete_all_cookies()
            logging.info('关闭窗口')
            self.browser.close()
            self.browser.switch_to.window(original_window)
            self.browser.refresh()
            time.sleep(random.randint(5, 10))

    def search(self, keyword='', max_pages=10):
        '''
        搜索关键词
        :param keyword:     关键词
        :param max_pages:   最大爬取的页数
        :return:
        '''
        # 等待搜索框加载完
        tb_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
        # 等待搜索按钮加载完成
        try:
            search_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > .search-button > button')))
        except Exception as e:
            search_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_SearchForm button')))

        tb_input.clear()
        tb_input.send_keys(keyword)
        logging.info('输入关键字【{}】'.format(keyword))

        time.sleep(random.randint(2, 5))
        search_btn.click()
        # 分页爬取商品信息
        self.get_list(max_pages, keyword)

    def get_list(self, max_page, keyword):
        '''获取每页的数据'''
        while max_page > 0:
            try:
                page_ele = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
                self.wait.until(
                    (EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item'))))
                html = self.browser.page_source
                html_eles = pq(html)

                # 处理商品信息
                items = html_eles('#mainsrp-itemlist .items .item').items()
                for item in items:
                    # 处理交易人数为整型
                    try:
                        product = {
                            'keyword': keyword,
                            'price': item.find('.price').text(),
                            'deal': item.find('.deal-cnt').text()[:-3],
                            'title': item.find('.title > a').text(),
                            'location': item.find('.location').text(),
                            'shop': item.find('.shop').text(),
                            'image': item.find('.pic img').attr('data-src'),
                        }
                        product['deal'] = product['deal'].replace('+', '')
                        if product['deal'].endswith('万'):
                            product['deal'] = int(product['deal'][-1]) * 10000
                        else:
                            product['deal'] = int(product['deal'])
                    except Exception as e:
                        product['deal'] = 0

                    print(product)

                max_page -= 1
                if max_page == 0:
                    break
                # 处理分页
                try:
                    next_btn = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager .next > a')))
                    next_btn.click()
                    logging.info(self.browser.current_url)
                    time.sleep(random.randint(5, 10))
                except Exception as e:
                    max_page = 0  # 没有分页，直接置为0， 不再爬取

            except Exception as e:
                pass

    def exit(self):
        logging.info('您已退出抓取系统!!!')
        self.browser.quit()

    def add_cookie_to_options(self, cookies):
        if cookies:
            for cookie in cookies:
                self.browser.add_cookie(cookie)

    def get_cookie(self):
        try:
            with open(self.COOKIE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            pass

    def set_cookie(self, _cookies):
        # 登录完成后，将cookie保存到本地文件
        with open(self.COOKIE_FILE, 'w') as f:
            f.write(json.dumps(_cookies))


if __name__ == '__main__':
    tb = Taobao('用户名', '密码')
    while True:
        keys = input('请输入要查询的关键词 + 爬取的最大页码以空格分隔如（粽子叶 5）：\n>>>:').strip()
        if keys == 'quit':
            tb.exit()
            break

        key, max_page = keys.split(' ')
        if key and str(max_page).isnumeric():
            try:
                tb.search(key, int(max_page))
            except Exception as e:
                print(e)
