#!/usr/bin/python
# -*- coding: <utf-8> -*-
# from gevent import monkey
# monkey.patch_all()
import requests
import re
import gevent
import time
import json
from concurrent.futures import ProcessPoolExecutor


def judge_result_exist(url_test: str) -> bool:
    """
    根据一条传入的url判断该条url是否存在可以爬取的信息
    :param url_test:传入的url
    :type url_test:str
    :return:判断的结果
    :rtype:bool
    """
    try:
        resp = requests.get(url_test, params=None).json()
        gevent.sleep(1)
        result_dict = resp['data']['results']
        if len(result_dict) > 0:
            return True
        else:
            return False
    except json.decoder.JSONDecodeError:
        return False


def parse_content(data_dict: dict, key_word: str) -> None:
    """
    根据传入的json数据进行分析提取，将有用的数据进行归纳存储
    :param data_dict: 包含有所有数据的字典
    :type data_dict: dict
    :param key_word: 将关键字手动传入到列表中
    :type key_word: str
    """
    data_result = data_dict['data']['results']
    for data in data_result:
        job = data['jobName']
        city = data['city']['items'][0]['name']
        salary = data['salary']
        exp = data['workingExp']['name']
        edu = data['eduLevel']['name']
        types = data['emplType']
        kw = key_word
        source = '智联招聘'

        result_list.append({
            'job': job,
            'city': city,
            'salary': salary,
            'exp': exp,
            'edu': edu,
            'types': types,
            'kw': kw,
            'source': source,
        })


def parse_single_base_url(base_url: str, kw: str):
    """
    判断该条url是否存在可以爬取的数据，并爬取这条url以及之后所有页数的内容
    :param base_url: 目标url
    :type base_url: str
    :param kw: 手动传递kw参数
    :type kw: str
    """
    start = 0
    base_url = re.sub('start=0', 'start={start}', base_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    while True:
        url = base_url.format(start=str(start))
        start += 90

        # 判断result中是否存在可爬取的数据
        if not judge_result_exist(url):
            break
        else:
            print(url)
            gevent.sleep(1)
            # data_dict = requests.get(url, headers=headers).json()
            # parse_content(data_dict, kw)


def gen_base_url_list(kw_list: list, salary_list: list):
    """
    根据一条基础的url和关键词以及薪资列表生成一个包含关键字的url列表
    :param kw_list: 包含所有关键字的列表
    :type kw_list: list
    :param salary_list: 包含所有薪资水平的列表
    :type salary_list: list
    """
    base_url = 'https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId=489&salary={salary}&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={kw}&kt=1&=1&at=42cf43ca7fc04d88978b24f369c9d7c2&rt=cdebee05f68b46ad9b2826ad59465995&_v=0.69931485&userCode=1011635495&x-zp-page-request-id=76b38778ef644e00a756a9a91249c2ba-1553191429933-939397'

    for kw in kw_list:
        for salary in salary_list:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            }
            base_url_list.append((base_url.format(salary=salary, kw=kw), kw))


if __name__ == '__main__':

    key_word_list = ['python', 'java', 'php', 'c', 'c++']
    salary_list = ['1,1000', '1001,2000', '2001,4000', '4001,6000', '6001,8000', '8001,10000', '10001,15000',
                   '15001,25000', '25001,35000', '35001,50000', '50001,70000', '70001,100000', '100001,999999']

    result_list = []
    base_url_list = []  # [(url, kw)]

    gen_base_url_list(key_word_list, salary_list)

    # for url, kw in base_url_list:
    #     parse_single_base_url(url, kw)

    start_time = time.time()
    # gevent.joinall([
    #     gevent.spawn(parse_single_base_url, url, kw) for url, kw in base_url_list])
    # with ProcessPoolExecutor(max_workers=4) as executor:
    #     for url, kw in base_url_list:
    #         executor.submit(parse_single_base_url, url, kw)
    for url, kw in base_url_list:
        parse_single_base_url(url, kw)

    print(len(base_url_list))
    print(time.time() - start_time)
