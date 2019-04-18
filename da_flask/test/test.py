# !/usr/bin/python
# -*- coding: <utf-8> -*-
__author__ = 'xiao'
__date__ = '2019/4/13 2:21 AM'


def get_top10_city():
    import pymysql
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='xzx199110',
        database='bs',
    )
    cursor = conn.cursor()
    sql = '''select city, count(*) num from bs_51job where not city="异地招聘" group by city order by num desc'''
    cursor.execute(sql)
    city_num_list = cursor.fetchall()

    return city_num_list


data_list = get_top10_city()


def strip_and_recount(data_list):
    new_list = []

    for data in data_list:
        new_list.append([data[0].replace(' ', ''), data[1]])

    finally_list = []
    city_list = []
    for num in range(len(new_list) - 1):
        city = new_list[num][0]
        if city not in city_list:
            city_list.append(city)
            city_num = new_list[num][1]
            for n in range(num + 1, len(new_list) - 2):
                if city in new_list[n][0]:
                    city_num += new_list[n][1]
            finally_list.append((city, city_num))

    return finally_list