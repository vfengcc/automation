import requests
import json
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
from douguo.handler_mongodb import mongo_info
# 创建队列

queue_list = Queue()

def handle_request(url, data):
    headers = {
        'client': '4',
        'version': '6959.2',
        'device': 'MI 9',
        'sdk': '25,7.1.2',
        'channel': 'baidu',
        'resolution': '1872*1080',
        'display-resolution': '1872*1080',
        'dpi': '2.0',
        # 'android-id': '13c46d86115b3392',
        # 'pseudo-id': 'd86115b339213c46',
        'brand': 'Xiaomi',
        'scale': '2.0',
        'timezone': '28800',
        'language': 'zh',
        'cns': '0',
        'carrier': 'CHINA+MOBILE',
        # 'imsi': '460071392411517',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; MI 9 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36',
        'act-code': '1586094259',
        'act-timestamp': '1586060747',
        'uuid': '55efd436-034a-4df7-aca4-bdafcc9ec96b',
        'battery-level': '0.78',
        'battery-state': '2',
        # 'mac': '08:00:27:AF:B7:64',
        'imei': '863254011059242',
        'terms-accepted': '1',
        'newbie': '1',
        'reach': '10000',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'Keep-Alive',
        # 'Cookie': 'duid=63838639',
        'Host': 'api.douguo.net',
        # 'Content-Length': '179'
    }

    response = requests.post(url, headers=headers, data=data)
    return response


def category():
    url = 'http://api.douguo.net/recipe/flatcatalogs'
    data = {
        'client': 4,
        # '_session': 1586066319728863254011059242,
        # 'v': 1586092322,
        '_vs': 2305,
        # 'sign_ran': '8b85545f6cc64b22a7bf6d7017406624',
        # 'code': 'add35aeffc7be7ed',
    }
    response = handle_request(url=url, data=data)
    index_response_dict = json.loads(response.text)
    for menu1_item in index_response_dict['result']['cs']:
        for menu2_item in menu1_item['cs']:
            for menu3_item in menu2_item['cs']:
                data_3 = {
                    # '_session': 1586066319728863254011059242,
                    '_vs': 11102,
                    'auto_play_mode': 2,
                    'client': 4,
                    # 'code': '7b23051e8829658d',
                    'keyword': menu3_item['name'],
                    'order': 0,
                    # 'sign_ran': '5c98550787ca2801919f7b234115b861',
                    'type': 0,
                }

                queue_list.put(data_3)

def list(data):
    print('当前处理的食材:{}'.format(data['keyword']))
    list_url = 'http://api.douguo.net/recipe/v2/search/0/20'
    list_response = handle_request(list_url, data=data)
    list_response_dict = json.loads(list_response.text)
    for item in list_response_dict['result']['list']:
        info = {}
        info['shicai'] = data['keyword']
        if item['type'] == 13:
            info['id'] = item['r']['id']
            info['author'] = item['r']['an']
            info['title'] = item['r']['n'].strip()
            info['intro'] = item['r']['cookstory'].replace('\n', '').replace(' ', '')
            info['foods'] = item['r']['major']
            info_url = 'http://api.douguo.net/recipe/detail/{}'.format(info['id'])
            info_data = {
                'client': 4,
                # '_session': 1586066319728863254011059242,
                'author_id': 0,
                '_vs': 11101,
                # 'is_new_user': 1,
                # 'sign_ran': '6705eaf45e868c98feb45786edae94b7',
                # 'code': 'cc997d9f53bfeb01',
            }
            info_re = handle_request(url=info_url, data=info_data)
            info_re_dict = json.loads(info_re.text)
            info['tips'] = info_re_dict['result']['recipe']['tips']
            info['cookstep'] = info_re_dict['result']['recipe']['cookstep']
            print('当前入库菜谱：{}'.format(info['title']))
            mongo_info.insert_item(info)
        else:
            continue


category()

# 最大20个线程
pool = ThreadPoolExecutor(max_workers=20)
while queue_list.qsize() > 0:
    pool.submit(list, queue_list.get())

print(queue_list.qsize())

# url = 'http://api.douguo.net/recipe/v2/search/0/20'
# data_3 = {
#     # '_session': 1586066319728863254011059242,
#     '_vs': 11102,
#     'auto_play_mode': 2,
#     'client': 4,
#     # 'code': '7b23051e8829658d',
#     'keyword': '手抓饼',
#     'order': 0,
#     # 'sign_ran': '5c98550787ca2801919f7b234115b861',
#     'type': 0,
# }
# re = handel_request(url, data=data_3)
# print(re.text)

