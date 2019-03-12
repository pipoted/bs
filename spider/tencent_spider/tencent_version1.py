#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from lxml import etree
from multiprocessing import Queue, Manager
from concurrent.futures import ThreadPoolExecutor
from gevent.pool import Pool
# import gevent
# from gevent.queue import Queue
import time

import pymysql


def get_meg_dict(content, result_list):
    print(len(content))
    tree = etree.HTML(content)

    trs = tree.xpath('//table[@class="tablelist"]/tbody/tr')[1:-1]

    for tr in trs:
        job = tr.xpath('.//a/text()')[0].strip()
        area = tr.xpath('.//td[4]/text()')[0].strip()
        typ = tr.xpath('.//td[2]/text()')[0].strip()
        # print(area, types)
        meg_dict = {
            'job': job,
            'area': area,
            'typ': str(typ),
        }
        print(meg_dict)
        result_list.append(meg_dict)
    id = tree.xpath('//a[@id="next"]/@href')[0]
    if 'javascript' in id:
        return None
    return 1


def save_to_sql(meg_dict):
    # print('save %s start' % meg_dict['job'], meg_dict['area'], meg_dict['typ'])
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='xzx199110',
        database='bs',
        port=3306,
    )
    cursor = conn.cursor()
    sql = """
    insert into tencent_test (job, area, typ) values (%s, %s, %s)"""
    try:
        cursor.execute(
            sql, (meg_dict['job'], meg_dict['area'], meg_dict['typ']))
        conn.commit()
    except TypeError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        # print('save %s end' % meg_dict['job'])


def get_all_meg(url, result_list):
    browser = webdriver.Chrome()
    browser.get(url)

    content = browser.page_source

    get_meg_dict(content, result_list)

    try:
        while True:
            browser.find_element_by_id('next').click()
            content = browser.page_source
            meg_dict = get_meg_dict(content, result_list)
            print(meg_dict)
            if meg_dict is None:
                raise Exception
    except Exception:
        browser.close()


# def create_result_list(queue_result, result_list):
#     while not queue_result.empty():
#         result_list.append(queue_result.get())
#     return result_list


if __name__ == '__main__':
    result_list = Manager().list()
    pool = Pool(size=15)
    url_list = ['https://job.tencent.com/position.php?keywords=&lid=0&tid=8%d' %
                num for num in range(1, 8, 1)]

    with ThreadPoolExecutor(max_workers=8) as executor:
        for url in url_list:
            executor.submit(get_all_meg, url, result_list)
        # executor.submit(create_result_list, queue_result, result_list)

    # gevent.joinall([gevent.spawn(get_all_meg, url, queue_result) for url in url_list])

    print(len(result_list))
    print('start saving')
    pool.map(save_to_sql, result_list)
    # with ThreadPoolExecutor(max_workers=8) as executor:
    #     executor.map(save_to_sql, result_list)
    print('saving success')
