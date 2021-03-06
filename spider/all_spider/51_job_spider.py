# !/usr/bin/python
# -*- coding: <utf-8> -*-
__author__ = 'xiao'
__date__ = '2019/3/26 4:45 PM'

import requests
from urllib import parse
import re
import time
import pymysql
from datetime import datetime
from lxml import etree


def log(func):
    '''用于记录日志信息的装饰器'''

    def inner(*args, **kwargs):
        print(func.__name__, 'is running', datetime.now())
        msg = str(datetime.now()) + '\t' + func.__name__ + \
            '\t' + str(args) + '\t' + str(kwargs) + '\n'
        with open('51job_log.txt', 'a') as fp:
            fp.write(msg)
        return func(*args, **kwargs)

    return inner


def save_to_mysql(data, conn) -> None:
    """将数据保存在mysql中"""
    cursor = conn.cursor()
    sql = """
    insert into bs_51job ( kw, job_name, company, city, salary, exp, edu) values (%s, %s, %s, %s, %s, %s, %s)
    """
    print('start save', data['job_name'])
    cursor.execute(sql, ( data['kw'], data['job_name'], data['company'], data['city'], data['salary'], data['exp'], data['edu']))
    conn.commit()
    time.sleep(0.05)


def get_total_page(url: str) -> int:
    """
    根据传入的url判断该条关键字一共有多少页
    :param url: url参数
    :type url: str
    """
    content = requests.get(url).content.decode('gb2312', errors='ignore')

    page_num = re.findall(pattern='共(\d+)页，到第', string=content)[0]
    return int(page_num)


def exist_data(url: str) -> bool:
    """
    判断给定url是否存在可以爬取的数据
    :param url: url参数
    :type url: str
    """
    content = requests.get(url).content.decode('gb2312', errors='ignore')
    if len(content) > 138000:
        return True
    else:
        return False


def parse_detail_url(url) -> tuple:
    """
    爬取详情页中edu与exp信息
    :param url: 详情页url
    :type url: str
    :return: 由两个信息组成的元组打包返回
    :rtype: tuple
    """
    content = requests.get(url).content.decode('gb2312', errors='ignore')
    tree = etree.HTML(content)
    data = tree.xpath('//p[@class="msg ltype"]/text()')[1:3]
    exp = data[0].replace('\xa0', ' ').strip()
    edu = data[1].replace('\xa0', ' ').strip()

    if '招' in edu:
        edu = '无要求'

    return exp, edu


def parse_url(url: str,  kw: str, conn) -> dict:
    """
    根据url爬取当前页面所有有用信息
    :param url: 目标url
    :type url: str
    :param job_type: 传递职位类型
    :type job_type: str
    """
    if not exist_data(url):
        return
    content = requests.get(url).content.decode('gb2312', errors='ignore')
    tree = etree.HTML(content)

    divs = tree.xpath('//div[@class="dw_table"]/div[@class="el"]')
    for div in divs:
        job_name = ''.join(div.xpath('./p/span/a/@title')).strip()
        company = ''.join(div.xpath('./span[1]/a/@title')).strip()
        city_tmp = ''.join(div.xpath('./span[2]/text()')).strip()
        city = re.sub('-.*?$', ' ', city_tmp)
        salary = ''.join(div.xpath('./span[3]/text()')).strip()
        url_temp = ''.join(div.xpath('./p/span/a/@href')).strip()

        try:
            exp, edu = parse_detail_url(url_temp)
        except IndexError:
            continue

        data_dict = {
            'kw': kw,
            'job_name': job_name,
            'company': company,
            'city': city,
            'salary': salary,
            'exp': exp,
            'edu': edu,
        }

        save_to_mysql(data_dict, conn)


def parse_every_page(url: str, kw: str, conn) -> list:
    """
    爬取每一条基础url所有页面的所有数据
    """
    page_num = get_total_page(url)
    data_list = []
    for page in range(1, page_num + 1):
        url = re.sub('2,(\d+).html', '2,' + str(page) + '.html', url)
        print('parse url', url)
        try:
            tmp_list = parse_url(url, kw, conn)
        except:
            continue
        if tmp_list is None:
            continue
        data_list += tmp_list

    return data_list


def gen_url_list() -> list:
    """
    生成需要爬取的url列表
    :return: 将url，关键字类型，关键字，职业类型放入元组中在统一存在列表中
    :rtype: list[tuple(str, str, str, str)]
    """
    key_lan_word = []
                    # java, python, c语言, c++，　ｓｑｌ，ｇｏ，ｐｈｐ,'c＃', 'JavaScript', 'perl', '．net', 'objective－c', 'MATLAB', 'R', 'assembly', 'swift', 'Delphi'
    key_job_word = ['运营', '大数据', '数据分析', '机器学习', '游戏制作', '人工智能']
                    # '前端', '后端', '软件开发', 'Android', 'ios', '测试', '运维', 'DBA', '算法', '架构',
    key_list = key_lan_word + key_job_word
    new_list = []
    for key in key_list:
        new_list.append(parse.quote(key))

    result_list = []

    base_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,{kw},2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=22&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

    for kw, kw_t in zip(new_list, key_list):
        result_list.append(
            (base_url.format(kw=kw), kw_t)
        )
    return result_list


if __name__ == '__main__':
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='xzx199110',
        database='bs',
        port=3306,
    )
    url_list = gen_url_list()

    for url, kw in url_list:
        parse_every_page(url, kw, conn)


    conn.close()
    # url = 'https://jobs.51job.com/hangzhou-yhq/111952527.html?s=01&t=0'
    # parse_detail_url(url)
