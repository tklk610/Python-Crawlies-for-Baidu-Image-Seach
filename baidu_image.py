import requests
from lxml import etree
import datetime
import time
import random
import os
import re

# -*- coding: utf-8 -*-

user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (WindowsNT 10.0; Win64; x64; rv:100.0) Gecko/20100101Firefox/100.0"
]



def  baidtu_uncomplie(url):
    res = ''
    c = ['_z2C$q', '_z&e3B', 'AzdH3F']
    d= {'w':'a', 'k':'b', 'v':'c', '1':'d', 'j':'e', 'u':'f', '2':'g', 'i':'h', 't':'i', '3':'j', 'h':'k', 's':'l', '4':'m', 'g':'n', '5':'o', 'r':'p', 'q':'q', '6':'r', 'f':'s', 'p':'t', '7':'u', 'e':'v', 'o':'w', '8':'1', 'd':'2', 'n':'3', '9':'4', 'c':'5', 'm':'6', '0':'7', 'b':'8', 'l':'9', 'a':'0', '_z2C$q':':', '_z&e3B':'.', 'AzdH3F':'/'}

    j= url

    for m in c :
        j = j.replace(m,d[m])
    for char in j :
        if re.match('^[a-w\d]+$', char):
            char = d[char]
        res= res + char
    return res


def get_images_from_baidu(keyword, page_num, save_dir):
    # UA 伪装：当前爬取信息伪装成浏览器
    # 将 User-Agent 封装到一个字典中
    # 【（网页右键 → 审查元素）或者 F12】 → 【Network】 → 【Ctrl+R】 → 左边选一项，右边在 【Response Hearders】 里查找

    headers = {
        'Accept'           : 'text/plain, */*; q=0.01',
        'User-Agent'       : random.choice(user_agent),
        'Accept-Encoding'  : 'gzip, deflate, br',
        'Connection'       : 'keep-alive',
        'X-Requested-With' : 'XMLHttpRequest'
    }

    # 请求的 url
    url = 'https://image.baidu.com/search/acjson'
    n   = 0
    image_list = []

    for i in range(0, page_num):
        # 请求参数
        pn  = 30 * i
        #gsm = int(pn, 16)

        param = {
            'tn'        : 'resultjson_com',
            'logid'     : '7603311155072595725',
            'ipn'       : 'rj',
            'ct'        : '201326592',
            'is'        : '',
            'fp'        : 'result',
            'fr'        : 'ala',
            'word'      : keyword,
            'queryWord' : keyword,
            'cl'        : '2',
            'lm'        : '1',
            'ie'        : 'utf-8',
            'oe'        : 'utf-8',
            'adpicid'   : '',
            'st'        : '',
            'z'         : '',
            'ic'        : '',
            'hd'        : '',
            'latest'    : '',
            'copyright' : '',
            's'         : '',
            'se'        : '',
            'tab'       : '',
            'width'     : '',
            'height'    : '',
            'face'      : '',
            'istype'    : '2',
            'qc'        : '',
            'nc'        : '',
            'expermode' : '',
            'cg'        : '',    # 这个参数没公开，但是不可少
            'pn'        : pn,    # 显示：30-60-90
            'rn'        : '30',  # 每页显示 30 条
            'gsm'       : '1e',
            '1618827096642': ''
            }

        request = requests.get(url=url, headers=headers, params=param)
        if request.status_code == 200:
            print('Request success.')

        request.encoding = 'utf-8'
        # 正则方式提取图片链接
        html = request.text
        with open('./wangye1.html', 'w', encoding='utf-8') as fp:
            fp.write(html)
        image_url_list = re.findall('"ObjUrl":"(.*?)",', html, re.S)

        for url in image_url_list :
            if url.startswith('https'):
                url = url.replace('\\', '')
            else :
                url = baidtu_uncomplie(url)

            image_list.append(url)

        time.sleep(random.randint(5, 10))


    print(image_list)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for image_url in image_list:
        image_data = requests.get(url=image_url, headers=headers).content
        with open(os.path.join(save_dir, f'{n:06d}.png'), 'wb') as fp:
            fp.write(image_data)
        n = n + 1

        time.sleep(random.randint(1, 10))


if __name__ == '__main__':
    keyword = "完美世界动漫"
    save_dir = keyword
    page_num = 2
    get_images_from_baidu(keyword, page_num, save_dir)
    print('Get images finished.')