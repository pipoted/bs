#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey

monkey.patch_all()
import requests
import gevent
import re
import pymysql
from lxml import etree


def save_to_mysql(data_dict):
    print(data_dict)
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='xzx199110',
        database='bs',
        port=3306,
    )
    cursor = conn.cursor(cursor=None)
    sql = """
    insert into boss_test (job, city, edu, exp, salary, company) values (%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(sql, (data_dict['job'], data_dict['city'], data_dict['edu'], data_dict['exp'], data_dict['salary'],
                         data_dict['company']))
    conn.commit()
    conn.close()


def get_content(url, content_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    content = resp.content.decode()
    # if 'next disabled' in content:
    #     raise BaseException
    content_list.append(content)


def ana_content_and_save(content):
    tree = etree.HTML(content)
    lis = tree.xpath('//div[@class="job-list"]/ul/li')
    for li in lis:
        job = li.xpath('.//div[@class="job-title"]/text()')[0].strip()
        city_tmp = li.xpath(
            './/div[@class="info-primary"]//p/text()')[0].strip()
        city = re.sub('\s(.*?)$', ' ', city_tmp)
        need = li.xpath('.//div[@class="info-primary"]//p/text()')[1:]
        edu = need[1].strip()
        exp = need[0].strip()
        salary = li.xpath('.//span[@class="red"]/text()')[0].strip()
        company = li.xpath(
            './/div[@class="info-company"]//h3//a/text()')[0].strip()

        data_dict = {
            'job': job,
            'city': city,
            'edu': edu,
            'exp': exp,
            'salary': salary,
            'company': company,
        }
        print('start save', data_dict['job'])
        save_to_mysql(data_dict)


def gen_url_list(kw_list, url_list: list):
    base_url = 'https://www.zhipin.com/c100010000/?query=%s&page=1&ka=page-1'
    for kw in kw_list:
        url_list.append(base_url % kw)


if __name__ == '__main__':
    url = 'https://www.zhipin.com/c100010000/?query=python&page=1&ka=page-1'
    kw_list = ['python', 'java', 'c', 'c++', 'php']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    url_list = []
    content_list = []

    print('start gen url')
    gen_url_list(kw_list, url_list)
    print('end gen url')

    print('start get content')
    task = []
    for url in url_list:
        page = 1
        print(url)
        while True:
            url = re.sub('page=(.*?)&', 'page=' + str(page) + '&', url)
            url = re.sub('=page-(\d+)$', '=page-' + str(page), url)
            print(url)
            if 'next disabled' not in requests.get(url, headers=headers).content.decode():
                # get_content(url, content_list)
                task.append(gevent.spawn(get_content, url, content_list))
                page += 1
            else:
                print('break', url)
                break

    gevent.joinall(task)

    print('start save content')
    # for content in content_list:
    #     ana_content_and_save(content)
    gevent.joinall([gevent.spawn(ana_content_and_save, content) for content in content_list])
    print('over')
