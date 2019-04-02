# !/usr/bin/python
# -*- coding: <utf-8> -*-
__author__ = 'xiao'
__date__ = '2019/3/27 2:08 AM'

import requests
import re
import pymysql
import time
from lxml import etree


def parse_every_url(url, kw, kw_type, conn) -> None:
    """爬取每条url每一页的内容"""
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }

    page = 1
    while True:
        url = re.sub('page=\d+', 'page=' + str(page), url)
        parse_one_url(url, kw, kw_type, conn)
        content = requests.get(url, headers=headers).content.decode()
        if not judge_next_page_exist(content):
            break
        else:
            page += 1

        time.sleep(300)


def gen_url_list():
    """返回需要爬取的url列表"""
    key_lan_word = ['python', 'java', 'c', 'c++', 'sql', 'go', 'php', 'c#', 'JavaScript', 'perl', '.net', 'objective-c',
                    'MATLAB', 'R', 'assembly', 'swift', 'Delphi']
    key_job_word = ['前端', '后端', '软件开发', 'Android',
                    'ios', '测试', '运维', 'DBA', '算法', '架构', '运营', '大数据', '数据分析', '机器学习', '游戏制作']
    result_list = []

    base_url = 'https://www.zhipin.com/c100010000/?query={kw}&page=1'

    for kw in key_lan_word:
        result_list.append(
            (base_url.format(kw=kw), kw, 'lan')
        )

    for kw in key_job_word:
        result_list.append(
            (base_url.format(kw=kw), kw, 'job')
        )

    return result_list


def judge_next_page_exist(content) -> bool:
    """判断是否存在需要爬取的下一页"""
    tree = etree.HTML(content)
    next_page = tree.xpath('//a[@class="next disabled"]')
    if next_page:
        return False
    else:
        return True


def parse_one_url(url: str, kw: str, kw_type: str, conn) -> None:
    """爬取单条url中所有所需的信息"""
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }
    content = requests.get(url, headers=headers).content.decode()
    tree = etree.HTML(content)

    lis = tree.xpath('//div[@class="job-list"]/ul/li')

    for li in lis:
        job_name = ''.join(
            li.xpath('.//h3[@class="name"]/a/div/text()')).strip()
        salary = ''.join(
            li.xpath('.//h3[@class="name"]/a/span/text()')).strip()
        city_tmp = li.xpath('.//div[@class="info-primary"]/p/text()')[0]
        city = re.sub('\s.*?\s.*?$', ' ', city_tmp).strip()
        exp = li.xpath('.//div[@class="info-primary"]/p/text()')[1].strip()
        edu = li.xpath('.//div[@class="info-primary"]/p/text()')[2].strip()
        company = ''.join(
            li.xpath('.//div[@class="company-text"]/h3/a/text()')).strip()
        data_dict = {
            'web': 'boss直聘',
            'kw': kw,
            'key_type': kw_type,
            'job_name': job_name,
            'salary': salary,
            'city': city,
            'exp': exp,
            'edu': edu,
            'company': company,
        }
        save_to_mysql(data_dict, conn)
        print(data_dict)
        time.sleep(1)
    time.sleep(5)


def save_to_mysql(data_dict: dict, conn) -> None:

    print('save test')
    cursor = conn.cursor()
    sql = """insert into boss_test (web, kw, key_type, job_name, salary, city, exp, edu, company) values
    (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (data_dict['web'], data_dict['kw'], data_dict['key_type'], data_dict['job_name'],
                         data_dict['salary'], data_dict['city'], data_dict['exp'], data_dict['edu'], data_dict['company']))
    conn.commit()
    time.sleep(1)


if __name__ == '__main__':
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='xzx199110',
        database='bs',
        port=3306,
    )
    url = 'https://www.zhipin.com/c100010000/s_306-t_805/?query=python&page=3&ka=page-3'
    url_list = gen_url_list()
    for url, kw, key_type in url_list:
        print('start base', url)
        parse_every_url(url, kw, key_type, conn)

    conn.close()
