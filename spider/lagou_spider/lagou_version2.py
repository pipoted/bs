#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Any

from selenium import webdriver
from lxml import etree
from random import randint
import gevent
import time
import pymysql
from multiprocessing import Manager


def judge_next_exist(browser_tmp: webdriver.Chrome):
    while True:
        browser.switch_to.window(browser.window_handles[randint(0, len(browser.window_handles) - 1)])
        content = browser_tmp.page_source
        tree = etree.HTML(content)
        next_page = tree.xpath('//span[@class="pager_next "]')
        if next_page:
            return True


def get_data(url_temp):
    browser.get(url_temp)
    browser.implicitly_wait(50)
    content = browser.page_source
    content_list.append(content)
    while True:
        time.sleep(2)
        print('over wait', url_temp)
        browser.implicitly_wait(50)
        content = browser.page_source
        content_list.append(content)
        print(len(content))
        tree = etree.HTML(content)
        next_page = tree.xpath('//span[@class="pager_next pager_next_disabled"]')
        if next_page:
            break
        print('test click next page')
        time.sleep(4)
        browser.find_element_by_class_name('pager_next ').click()
        print('click success')
        time.sleep(2)


def get_detail_href(content: str):
    tree = etree.HTML(content)

    lis = tree.xpath('//ul[@class="item_con_list"]/li')
    for li in lis:
        href = ''.join(li.xpath('.//a[@class="position_link"]/@href'))
        get_detail_href_content(href)
    print('list over')
    return


def get_detail_href_content(href):
    time.sleep(5)
    browser.get(href)
    browser.implicitly_wait(50)
    browser.find_element_by_class_name('name')
    parse_detail_href(browser.page_source)


def parse_detail_href(content):
    tree = etree.HTML(content)
    job = ''.join(tree.xpath('//span[@class="name"]/text()')).strip()
    ps = tree.xpath('//dd[@class="job_request"]/p[1]')[0]
    salary = ''.join(ps.xpath('./span[1]/text()')).strip()
    area = ''.join(ps.xpath('./span[2]/text()')).replace('/', '').strip()
    req = ''.join(ps.xpath('./span[3]/text()')).replace('/', '').strip()
    edu = ''.join(ps.xpath('./span[4]/text()')).replace('/', '').strip()
    types = ''.join(ps.xpath('./span[5]/text()')).strip()
    result_list.append({
        'job': job,
        'salary': salary,
        'area': area,
        'req': req,
        'edu': edu,
        'types': types
    })
    print(len(result_list))


def save_to_mysql(data: dict):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='xzx199110',
        database='bs',
        port=3306,
    )
    cursor = conn.cursor()
    sql = """insert into lagou_test (job, salary, area, req, edu, types) values (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (data['job'], data['salary'], data['area'], data['req'], data['edu'], data['types']))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # 183.148.135.118:9999
    browser = webdriver.Chrome()
    kw_list = ['java']
    city_list = ['北京']
    kd_list = []
    for kw in kw_list:
        for city in city_list:
            kd_list.append((kw, city))
    # noinspection PyRedeclaration
    content_list = Manager().list()
    href_list = Manager().list()
    result_list = Manager().list()

    url = 'https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput='
    url_list = [url.format(kw, city) for kw, city in kd_list]

    for url in url_list:
        get_data(url)

    for content in content_list:
        get_detail_href(content)

    # with ThreadPoolExecutor(max_workers=4) as executor:
    #     for url in url_list:
    #         executor.submit(get_data, url, content_list, browser)
    # gevent.joinall([
    #     gevent.spawn(get_data, url, content_list, browser) for url in url_list
    # ])

    browser.quit()
    print(result_list)
