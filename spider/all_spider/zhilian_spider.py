# !/usr/bin/python
# -*- coding: <utf-8> -*-

import requests
import json
import time
import re
import pymysql


def save_to_mysql(data: dict, conn):
    cursor = conn.cursor()
    if '-' in data['city']:
        data['city'] = re.sub('-.*?$', ' ', data['city']).strip()
    print('start save', data['job_name'], data['kw'], data['city'])
    sql = '''
    insert into zhilian_job (kw, job_name, company, city, salary, exp, edu) values (%s,%s,%s,%s,%s,%s,%s)
    '''
    cursor.execute(sql, (
    data['kw'], data['job_name'], data['company'], data['city'], data['salary'], data['exp'], data['edu']))
    conn.commit()
    time.sleep(1)


def get_data(url: str, kw: str, conn):
    '''提取该条url中所有可以提取的数据'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    content = requests.get(url, headers=headers).content.decode()
    data_list = json.loads(content)['data']['results']
    for data in data_list:
        job_name = data['jobName']
        company = data['company']['name']
        city = data['city']['display']
        salary = data['salary']
        exp = data['workingExp']['name']
        edu = data['eduLevel']['name']

        data_dict = {
            'kw': kw,
            'job_name': job_name,
            'company': company,
            'city': city,
            'salary': salary,
            'exp': exp,
            'edu': edu,
        }

        save_to_mysql(data_dict, conn)


def judge_result_data_exist(content: str):
    '''判断该页是否存在可以爬取的数据，存在返回True，否则返回false'''
    try:
        data_list = json.loads(content)['data']['results']
    except:
        return False
    if len(data_list) != 0:
        return True
    else:
        return False


def loop_spider(url: str, kw: str, conn):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    page = 0
    while True:
        url = re.sub('start=\d+&', 'start=' + str(page) + '&', url)
        print('start this', url)
        content = requests.get(url, headers=headers).content.decode()
        flag = judge_result_data_exist(content)
        if flag:
            get_data(url, kw, conn)
            continue
            page += 90
        else:
            break


def gen_url_list():
    base_url = '''https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId=489&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={kw}&kt=3&=0&rt=cdebee05f68b46ad9b2826ad59465995&_v=0.67395132&x-zp-page-request-id=4e016822e03b42238ccdde80f80db89f-1554534268499-442740'''
    key_lan_word = ['python', 'java', 'c语言', 'c++', 'sql', 'go', 'php', 'c#', 'JavaScript', 'perl', '.net', 'objective-c',
                    'MATLAB', 'R', 'assembly', 'swift', 'Delphi']
    key_job_word = ['前端', '后端', '软件开发', 'Android',
                    'ios', '测试', '运维', 'DBA', '算法', '架构', '运营', '大数据', '数据分析', '机器学习', '游戏制作', '人工智能']
    key_list = key_lan_word + key_job_word
    result_list = []

    for kw in key_list:
        result_list.append((base_url.format(kw=kw), kw))

    return result_list


if __name__ == '__main__':
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='xzx199110',
        database='bs',
        port=3306,
    )
    url_list = gen_url_list()

    for url, kw in url_list:
        loop_spider(url, kw, conn)

    conn.close()
