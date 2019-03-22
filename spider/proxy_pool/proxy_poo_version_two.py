# !/usr/bin/python
# -*- coding: <utf-8> -*-
__author__ = 'xiao'
__date__ = '2019/3/22 12:23 PM'

import requests
import re
from lxml import etree


def get_proxy(url_tmp):
    content = requests.get(url_tmp).content.decode()
    tree = etree.HTML(content)

    ips = tree.xpath('//td[@data-title="IP"]/text()')
    ports = tree.xpath('//td[@data-title="PORT"]/text()')
    types = tree.xpath('//td[@data-title="类型"]/text()')
    times = tree.xpath('//td[@data-title="响应速度"]/text()')

    proxy_list = []
    for ip, port, typ, time in zip(ips, ports, types, times):
        time = re.sub('秒', '', time)
        if float(time) > 2.0:
            continue
        proxy_list.append([ip, port, typ.lower(), float(time)])

    return proxy_list


def ip_test(proxies: dict):
    url = 'http://icanhazip.com/'
    requests.adapters.DEFAULT_RETRIES = 3
    try:
        resp = requests.get(url, timeout=3, proxies=proxies)
    except BaseException:
        return False
    else:
        return True


def gen_proxy_dict(p_list: list):
    return {
        'HTTP': p_list[2] + '://' + p_list[0] + ':' + p_list[1],
        'HTTPS': p_list[2] + '://' + p_list[0] + ':' + p_list[1],
    }


def main():
    url_list = ['https://www.kuaidaili.com/free/inha/1/',
                'https://www.kuaidaili.com/free/inha/2/']
    proxy_list = []
    proxy_dict = []
    for url in url_list:
        proxy_list += get_proxy(url)

    for p_list in proxy_list:
        proxy_dict += gen_proxy_dict(p_list)

    return proxy_dict


def return_one_proxy():
    proxy_list = main()
    while True:
        if len(proxy_list) > 5:
            proxy = proxy_list.pop()
            print('proxy testing')
            if ip_test(proxy):
                return proxy
        else:
            proxy_list = main()


if __name__ == '__main__':
    print(return_one_proxy())
