#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import time
from concurrent.futures import ThreadPoolExecutor


def get_data(url_temp, con_list, browser):
    browser.get(url_temp)
    while True:
        time.sleep(7)
        print('over wait', url_temp)
        browser.implicitly_wait(50)
        try:
            browser.find_element_by_class_name('pager_next ').click()
            print('click success')
        except:
            continue
        content = browser.page_source
        print(content)
        tree = etree.HTML(content)
        next_page = tree.xpath('//span[@class="pager_next pager_next_disabled"]')
        if next_page:
            break
        con_list.append(content)
    browser.close()


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    content_list = []
    kw_list = ['java', 'python', 'c', 'c++', 'php']
    city_list = ['北京', '上海', '广州', '深圳']
    kd_list = []
    for kw in kw_list:
        for city in city_list:
            kd_list.append((kw, city))
    content_list = []

    url = 'https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput='
    url_list = [url.format(kw, city) for kw, city in kd_list]

    with ThreadPoolExecutor(max_workers=4) as executor:
        for url in url_list:
            executor.submit(get_data, url, content_list, browser)

    browser.quit()
    print(len(content_list))
