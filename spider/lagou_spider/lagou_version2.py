#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from lxml import etree
import time


url = 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?px=default&city=%E5%85%A8%E5%9B%BD'
browser = webdriver.Chrome()
browser.get(url)

content = browser.page_source
tree = etree.HTML(content)
lis = tree.xpath('//div[@class="s_position_list "]/ul/li')

# for li in lis:
#     job = li.xpath('.//a[@class="position_link"]/h3/text()')[0].strip()
#     money = li.xpath('.//span[@class="money"]/text()')[0].strip()
#     need = li.xpath('.//div[@class="li_b_l"]/text()')[2].strip()
#     company = li.xpath('.//div[@class="company_name"]/a/text()')[0].strip()
#     meg_dict = {
#         'job': job,
#         'money': money,
#         'need': need,
#         'company': company,
#     }
#     print(meg_dict)
#     break

content_list = []
try:
    while True:
        time.sleep(0.5)
        browser.find_element_by_class_name('pager_next ').click()
        content = browser.page_source
        content_list.append(content)
except:
    time.sleep(15)
finally:
    browser.close()
