#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import pymysql
import asyncio
import re
import multiprocessing as mul
from gevent.pool import Pool
from multiprocessing import Manager
from concurrent.futures import ThreadPoolExecutor


def get_content(url, content_list):
    content = requests.get(url).content.decode()
    content_list.append(content)


def get_use_msg(content, result_list):
    content_dict = json.loads(content)
    data_dict = content_dict['data']['results']
    if len(data_dict) == 0:
        raise IndexError
    for data in data_dict:
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


def save_to_sql(dic):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='xzx199110',
        database='bs',
        port=3306,
    )
    cursor = conn.cursor()
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
    url = re.sub('&kw=(.*?)&', kw, url, count=0, flags=0)
    url = re.sub('&salary=(.*?),[\d]+&', salary[0], url, count=0, flags=0)
    url = re.sub('&salary=[\d]+,(.*?)&', salary[1], url)
    return url


def gen_kw_url_list(base_url, salary_list, kw_list):
    url_list = Manager().list()

    with ThreadPoolExecutor(max_workers=5) as executor:
        for kw in kw_list:
            for salary in salary_list:
                executor.submit(gen_one_list, base_url, salary, kw)


if __name__ == '__main__':
    url = '''https://fe-api.zhaopin.com/c/i/sou?start=90&pageSize=90&cityId=489&salary=1,1000&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3&=1&_v=0.54277500&x-zp-page-request-id=20aa3cf26b9d4d05b4aaafe175de0c6d-1552385870753-809381'''
    salary_list = [(1, 1000), (1001, 2000), (2001, 4000), (4001, 6000),
                   (6001, 8000), (8001, 10000), (10001, 15000), (15001, 25000),
                   (25001, 35000), (35001, 50000), (50001, 70000), (70001, 100000),
                   (100001, 999999)]
    kw_list = ['python', 'java', 'c', 'c++']
    result_list = Manager().list()
    content_list = Manager().list()

    get_content(url, content_list)
    get_use_msg(content_list.pop(), result_list)

    pool = Pool(size=10, greenlet_class=None)

    pool.map(save_to_sql, result_list)
