# coding=utf-8
__author__ = 'xiao'
__date__ = '2019/3/19 10:59 AM'

import requests
import re
import time
from lxml import etree


def get_url_list():
    kw_list = ['python', 'java', 'c', 'c++']
    url = 'https://search.51job.com/list/010000,000000,0000,00,9,{num},{kw},2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=21&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    url_list = []

    for kw in kw_list:
        for num in range(1, 12):
            if num < 10:
                num = '0' + str(num)
            else:
                num = str(num)
            url_list.append(url.format(num=num, kw=kw))

    return url_list


def get_page_num(url):
    content = requests.get(url).content.decode(encoding='gbk')
    tree = etree.HTML(content)

    num = tree.xpath('//div[@class="p_in"]/span[1]/text()')
    num = ''.join(num)
    num = ''.join(re.findall('共(\d+)页', num))
    return num


def get_data(url):
    content = requests.get(url).content.decode(encoding='gbk')
    tree = etree.HTML(content)
    els = tree.xpath('//div[@class="el"]')

    data_list = []
    for el in els:
        job = ''.join(el.xpath('.//p/span/a/@title')).strip()
        area = ''.join(el.xpath('.//span[@class="t3"]/text()'))
        area = re.sub('-.*?$', ' ', area).strip()
        salary = ''.join(el.xpath('.//span[@class="t4"]/text()')).strip()

        if job == '' or area == '' or salary == '':
            continue

        data_dict = {
            'job': job,
            'area': area,
            'salary': salary,
        }
        data_list.append(data_dict)

    return data_list


if __name__ == '__main__':
    data_list = []
    for url in get_url_list():
        for page in range(1, int(get_page_num(url)) + 1):
            url = re.sub(',(\d+).html', ',' + str(page) + '.html', url)
            print('start spider', url)
            data_list += get_data(url)
            time.sleep(3)
        time.sleep(3)

    print(data_list)
