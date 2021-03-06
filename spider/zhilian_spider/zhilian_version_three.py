#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey

monkey.patch_all()
import requests
import json
import re
import gevent
import pymysql
from gevent.pool import Pool

'''
协程测试
'''


def generate_url_list(base_url, kw_list, salary_list, url_list):
    for kw in kw_list:
        for salalry in salary_list:
            url = base_url % (str(salalry[0]), str(salalry[1]), str(kw))
            url_list.append(url)


def get_msg_data(url, data_list):
    content = requests.get(url).content
    kw = re.findall('&kw=(.*?)&', url)[0]
    print(len(content))
    data = json.loads(content)

    data_dict = data['data']['results']
    data_dict.append(kw)
    data_list.append(data_dict)


def get_msg(data_dict, conn):
    kw = data_dict.pop()
    for data in data_dict:
        job = data['jobName']
        city = data['city']['items'][0]['name']
        work_exp = data['workingExp']['name']
        edu = data['eduLevel']['name']
        salary = data['salary']
        company = data['company']['name']
        empl_type = data['emplType']
        msg_dict = {
            'kw': kw,
            'job': job,
            'city': city,
            'work_exp': work_exp,
            'edu': edu,
            'salary': salary,
            'company': company,
            'empl_type': empl_type,
        }
        print('save', msg_dict['job'])
        save_to_sql(msg_dict, conn)


def start_spider_url(url, data_list):
    start = 0
    # proxies = {
    #     'http': 'http://125.40.109.154:31610',
    #     'https': 'https://110.52.235.214:9999',
    # }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    while True:
        url = re.sub('\?start=\d+&', '?start=' + str(start) + '&', url)
        gevent.sleep(1)
        if len(requests.get(url, headers=headers).content.decode()) > 17090:
            start += 90
            get_msg_data(url, data_list)
        else:
            return


def save_to_sql(msg_dict, conn):
    cursor = conn.cursor()
    sql = """
    insert into zhilian_test (kw, job, city, work_exp, edu, salary, company, empl_type) values
    (%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(sql, (
        msg_dict['kw'], msg_dict['job'], msg_dict['city'], msg_dict['work_exp'], msg_dict['edu'], msg_dict['salary'],
        msg_dict['company'], msg_dict['empl_type']))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    url = 'https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId=489&salary=%s,%s&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=%s&kt=3&=1&_v=0.54277500&x-zp-page-request-id=20aa3cf26b9d4d05b4aaafe175de0c6d-1552385870753-809381'
    kw_list = ['java', 'python', 'c', 'c++', 'php']
    salary_list = [(1, 1000), (1001, 2000), (2001, 4000), (4001, 6000),
                   (6001, 8000), (8001, 10000), (10001, 15000), (15001, 25000),
                   (25001, 35000), (35001, 50000), (50001, 70000), (70001, 100000),
                   (100001, 999999)]
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='xzx199110',
        database='spider',
        port=3306,
    )
    url_list = []
    data_list = []
    pool = Pool(10)

    generate_url_list(url, kw_list, salary_list, url_list)
    # for url in url_list:
    #     print('start url', url)
        # start_spider_url(url, data_list)
    gevent.joinall([gevent.spawn(start_spider_url, url, data_list) for url in url_list])
    print('test')

    print('start')
    # for data_dict in data_list:
    #     get_msg(data_dict, conn)

    gevent.joinall([gevent.spawn(data_dict, conn) for data_dict in data_list])
