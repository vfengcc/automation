import re
import requests
import time
from lxml import etree
from handler_db import handler_get_task

def special_decode(content):
    regex_list = [
        {'name': [' &#xe603; ', ' &#xe60d; ', ' &#xe616; '], 'value': 0},
        {'name': [' &#xe602; ', ' &#xe60e; ', ' &#xe618; '], 'value': 1},
        {'name': [' &#xe605; ', ' &#xe610; ', ' &#xe617; '], 'value': 2},
        {'name': [' &#xe604; ', ' &#xe611; ', ' &#xe61a; '], 'value': 3},
        {'name': [' &#xe606; ', ' &#xe60c; ', ' &#xe619; '], 'value': 4},
        {'name': [' &#xe607; ', ' &#xe60f; ', ' &#xe61b; '], 'value': 5},
        {'name': [' &#xe608; ', ' &#xe612; ', ' &#xe61f; '], 'value': 6},
        {'name': [' &#xe60a; ', ' &#xe613; ', ' &#xe61c; '], 'value': 7},
        {'name': [' &#xe60b; ', ' &#xe614; ', ' &#xe61d; '], 'value': 8},
        {'name': [' &#xe609; ', ' &#xe615; ', ' &#xe61e; '], 'value': 9},
    ]
    for i in regex_list:
        for j in i['name']:
            content = re.sub(j, str(i['value']), content)
    return content


def parser_html(content):
    content = special_decode(content)
    html = etree.HTML(content)
    user_info = {}
    user_info['uid'] = int(html.xpath("//div[@class='personal-card']//div[@class='info1']//span[@data-id]/@data-id")[0])
    id1 = html.xpath("//p[@class='shortid']/text()")[0].strip()
    id2 = ''.join(html.xpath("//p[@class='shortid']/i/text()"))
    user_info['dyid'] = re.sub(r'抖音ID：', '', id1 + id2).strip()
    user_info['dyname'] = html.xpath("//p[@class='nickname']/text()")[0].strip()
    user_info['dyverify'] = ''
    if html.xpath("//div[@class='info2']//span[@class='info']/text()"):
        user_info['dyverify'] = html.xpath("//div[@class='info2']//span[@class='info']/text()")[0].strip()
    user_info['dysign'] = html.xpath("//div[@class='info2']//p[@class='signature']/text()")[0].strip()
    ele_follow = html.xpath("//p[@class='follow-info']")[0]

    user_info['follows'] = ''.join(ele_follow.xpath("//span[contains(@class, 'focus')]//i/text()")).strip()
    user_info['fans'] = ''.join(ele_follow.xpath("//span[contains(@class, 'follower')]//i/text()")).strip()
    user_info['likes'] = ''.join(ele_follow.xpath("//span[contains(@class, 'liked-num')]//i/text()")).strip()
    try:
        if ele_follow.xpath("//span[contains(@class, 'follower')]//span[@class='num']/text()")[-1].strip() == 'w':
            user_info['fans'] = str(int(user_info['fans']) / 10) + 'w'
    except Exception as e:
        pass

    try:
        if ele_follow.xpath("//span[contains(@class, 'liked-num')]//span[@class='num']/text()")[-1].strip() == 'w':
            user_info['likes'] = str(int(user_info['likes']) / 10) + 'w'
    except Exception as e:
        pass

    user_info['works'] = ''.join(html.xpath("//div[contains(@class, 'user-tab')]//span[@class='num']/i/text()")).strip()
    user_info['like_works'] = ''.join(html.xpath("//div[contains(@class, 'like-tab')]//span[@class='num']/i/text()")).strip()
    return user_info


def handle_douyin_web_share(task):
    # url = 'https://www.iesdouyin.com/share/user/61529182031'
    url = 'https://www.iesdouyin.com/share/user/{}'.format(task['share_id'])
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

    re = requests.get(url=url, headers=headers)
    return parser_html(re.text)


if __name__ == '__main__':
    while True:
        task = handler_get_task()
        user_info = handle_douyin_web_share(task)
        print(user_info)
        time.sleep(1)

