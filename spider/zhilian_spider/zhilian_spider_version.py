#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import pymysql
import re
import gevent
import multiprocessing as mul
from gevent.pool import Pool
from multiprocessing import Manager, Process
from concurrent.futures import ThreadPoolExecutor


def get_content(url, content_list):
    print('start spider:', url)
    content = requests.get(url).content.decode()
    print(len(content))
    if len(content) < 500:
        raise IndexError
    content_dict = json.loads(content)
    data_dict = content_dict['data']['results']
    content_list.append(data_dict)


def get_use_msg(content, result_list):
    for data in content:
        job = data['jobName']
        city = data['city']['items'][0]['name']
        work_exp = data['workingExp']['name']
        edu = data['eduLevel']['name']
        salary = data['salary']
        company = data['company']['name']
        empl_type = data['emplType']
        msg_dict = {
            'job': job,
            'city': city,
            'work_exp': work_exp,
            'edu': edu,
            'salary': salary,
            'company': company,
            'empl_type': empl_type,
        }
        result_list.append(msg_dict)


def thread_run_get_msg(content_list, result_list):
    for content in content_list:
        get_use_msg(content, result_list)


def save_to_sql(dic):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='xzx199110',
        database='bs',
        port=3306,
    )
    cursor = conn.cursor()
    print('start save ', dic['job'])
    sql = """
    insert into zhilian_test (job, city, work_exp, edu, salary, company,
     empl_type) values (%s, %s, %s, %s, %s, %s, %s)"""
    try:
        cursor.execute(sql, (dic['job'], dic['city'], dic['work_exp'],
                             dic['edu'], dic['salary'], dic['company'], dic['empl_type']))
        conn.commit()
    except Exception as e:
        print(e)


def gen_one_list(url: str, salary: tuple, kw: str, url_list):
    url = re.sub('&kw=(.*?)&', '&kw=' + kw + '&', url, count=0, flags=0)
    url = re.sub('&salary=[\d]+,(.*?)&', '&salary=' + str(salary[0]) + ',' + str(salary[1]) + '&', url)
    print('gen', url)
    url_list.append(url)


def gen_kw_url_list(base_url, salary_list, kw_list, url_list):
    for kw in kw_list:
        for salary in salary_list:
            print('gen ', kw, salary)
            gen_one_list(base_url, salary, kw, url_list)


def thread_run_get_content(url_list, content_list):
    start = 0
    for url in url_list:
        while True:
            url = re.sub('\?start=(\d+)', '?start=' + str(start), url, count=0, flags=0)
            start += 90
            try:
                get_content(url, content_list)
            except BaseException:
                print(url, 'wrong')
                break
    print('test')


if __name__ == '__main__':
    url = '''https://fe-api.zhaopin.com/c/i/sou?start=90&pageSize=90&cityId=489&salary=1,1000&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3&=1&_v=0.54277500&x-zp-page-request-id=20aa3cf26b9d4d05b4aaafe175de0c6d-1552385870753-809381'''
    salary_list = [(1, 1000), (1001, 2000), (2001, 4000), (4001, 6000),
                   (6001, 8000), (8001, 10000), (10001, 15000), (15001, 25000),
                   (25001, 35000), (35001, 50000), (50001, 70000), (70001, 100000),
                   (100001, 999999)]
    kw_list = ['python', 'java', 'c', 'c++']
    result_list = Manager().list()
    content_list = Manager().list()
    url_list = Manager().list()

    print('start get gen url')
    p1 = Process(target=gen_kw_url_list, args=(url, salary_list, kw_list, url_list))
    p2 = Process(target=thread_run_get_content, args=(url_list, content_list))
    p3 = Process(target=thread_run_get_msg, args=(content_list, result_list))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    pool = Pool(size=10, greenlet_class=None)

    print('start save')
    pool.map(save_to_sql, result_list)
    print('save over')
