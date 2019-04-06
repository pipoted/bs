#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import etree
import requests

url = 'https://www.zhipin.com/c100010000/s_306-t_805/?query=python&page=3&ka=page-3'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
}


content = requests.get(url, headers=headers).content.decode()

tree = etree.HTML(content)
next_page = tree.xpath('//a[@class="next"]')
if next_page:
    print('false')
    print(next_page)
else:
    print(next_page)
    print('true')
