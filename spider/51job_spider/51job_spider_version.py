# coding=utf-8
__author__ = 'xiao'
__date__ = '2019/3/19 10:59 AM'

import requests
import re
import time
import pymysql
import gevent
from multiprocessing import Manager
from lxml import etree


def get_url_list():
    """
    根据基础url生成url列表，并返回
    :return: url列表
    :rtype: list
    """
    kw_list = ['python', 'java', 'c', 'c++', 'ruby', 'php', 'c#', '前端', '测试']
    url = 'https://search.51job.com/list/000000,000000,0000,00,9,{num},{kw},2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=21&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    url_list = []

    for kw in kw_list:
        for num in range(1, 12):
            if num < 10:
                num = '0' + str(num)
            else:
                num = str(num)
            url_list.append((kw, url.format(num=num, kw=kw)))

    return url_list


def get_page_num(url_tmp: str) -> str:
    """
    从url中提取页数信息并返回
    :param url_tmp: 目标url
    :type url_tmp: str
    :return: 页数
    :rtype: str
    """
    content = requests.get(url_tmp).content.decode(encoding='gbk')
    tree = etree.HTML(content)

    num = tree.xpath('//div[@class="p_in"]/span[1]/text()')
    num = ''.join(num)
    num = ''.join(re.findall('共(\d+)页', num))
    return num


def get_data(url_tmp: str, kw_tmp: str, list_tmp: Manager().list()) -> None:
    """
    根据传入的url提取URL中的信息并存储在mysql中
    :param kw_tmp: 船体kw值
    :type kw_tmp: str
    :param url_tmp: 目标url
    :type url_tmp: str
    """
    content = requests.get(url_tmp).content.decode(encoding='gbk')
    tree = etree.HTML(content)
    els = tree.xpath('//div[@class="el"]')
    print(kw)

    for el in els:
        job = ''.join(el.xpath('.//p/span/a/@title')).strip()
        area = ''.join(el.xpath('.//span[@class="t3"]/text()'))
        area = re.sub('-.*?$', ' ', area).strip()
        salary = ''.join(el.xpath('.//span[@class="t4"]/text()')).strip()

        if job == '' or area == '' or salary == '':
            continue

        data_dict = {
            'kw': kw_tmp,
            'job': job,
            'area': area,
            'salary': salary,
        }
        list_tmp.append(data_dict)


def thread_run_spider(url_tmp, kw_tmp, list_temp):
    """
    提取每条url中包含多少页数，并按照页数循环提取每页数据
    :param url_tmp: 目标url
    :type url_tmp: str
    :param kw_tmp: 传递kw信息
    :type kw_tmp: str
    """
    page_all = int(get_page_num(url_tmp))
    for page in range(1, page_all + 1):
        url_tmp = re.sub(',(\d+).html', ',' + str(page) + '.html', url_tmp)
        print('start spider', url_tmp)
        get_data(url_tmp, kw_tmp, list_temp)
        time.sleep(3)
    time.sleep(3)


def save_to_mysql(cursor_tmp, data):
    """
    将传递的data dict 存储在mysql中
    :param cursor_tmp: cursor对象
    :type cursor_tmp:
    :param data: 目标dict
    :type data: dict
    """
    print('start save', data['job'])
    sql = """
    insert into 51_test (kw, job, area, salary) values (%s, %s, %s, %s)"""

    cursor_tmp.execute(sql, (data['kw'], data['job'], data['area'], data['salary']))
    conn.commit()


if __name__ == '__main__':
    data_list = Manager().list()
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='xzx199110',
        database='bs',
        port=3306,
    )
    cursor = conn.cursor()
    with ThreadPoolExecutor(max_workers=8) as executor:
        for kw, url in get_url_list():
            executor.submit(thread_run_spider, url, kw, data_list)

    print('start save')
    gevent.joinall([gevent.spawn(save_to_mysql(cursor, data)) for data in data_list])
    conn.close()
