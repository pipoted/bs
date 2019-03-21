#!/usr/bin/python
# -*- coding: <utf-8> -*-
import requests
from lxml import etree

url = 'https://sou.zhaopin.com/?p=2&jl=489&sf=1&st=1000&et=2&kw=python&kt=1'

data = requests.get(url).content.decode()
print(data)


def judge_next_page_exist(data: str) -> bool:
    """
    给定当前页面的文本，判断是否存在下一页，存在返回True
    :param data: 当前页面文本
    :type data: str
    :return: 存在下一页返回True
    :rtype: bool
    """
    tree = etree.HTML(data)
    not_next_page = tree.xpath(
        '//button[@class="btn soupager__btn soupager__btn--disable"]')

    if not_next_page:
        return False
    else:
        return True


def parse_content(data_tmp):
    pass
