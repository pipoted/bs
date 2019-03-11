#!/usr/bin/env python
# -*- coding: utf-8 -*-


from selenium import webdriver
from lxml import etree

from multiprocessing import Queue


def create_browser_obj(url):
    browser = webdriver.Chrome()
    browser.get(url)
    return browser


def get_page_source(browser):
    return browser.page_source


def ana_content(content, queue_result):
    tree = etree.HTML(content)

    try:
        lis = tree.xpath('//div[@class="s_position_list "]/ul/li')
        for li in lis:
            job = li.xpath('.//a[@class="position_link"]/h3/text()')[0].strip()
            money = li.xpath('.//span[@class="money"]/text()')[0].strip()
            need = li.xpath('.//div[@class="li_b_l"]/text()')[2].strip()
            company = li.xpath('.//div[@class="company_name"]/a/text()')
            meg_dict = {
                'job': job,
                'money': money,
                'need': need,
                'company': company,
            }
            queue_result.put_nowait(meg_dict)
    except:
        return


def get_next_page(browser):
    try:
        browser.find_element_by_class_name('pager_next ').click()
        gevent.sleep(0)
        return browser
    except:
        return None


def get_all_content(browser, queue_content):
    while get_next_page(browser):
        queue_content.put_nowait(browser.page_source)


def save_to_sql(dic):
    pass


def save_to_mongo(dic):
    pass


if __name__ == '__main__':
    queue_result = Queue()
    queue_content = Queue()
    url = 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?px=default&city=%E5%85%A8%E5%9B%BD#filterBox'
    browser = create_browser_obj(url)
    queue_content.put_nowait(get_page_source(browser))

    print('get all content start')
    get_all_content(browser, queue_content)
    print('get all content end')

    print('ana all content start')
    for content in queue_content.get_nowait():
        ana_content(content, queue_result)

    print('ana all content end')

    print('start print')
    for i in queue_result.get_nowait():
        print(i)

    print('all over')


