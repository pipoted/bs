#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyecharts import Geo, Page, Style
import pymysql


def get_data(kw):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='xzx199110',
        database='bs'
    )

    cursor = conn.cursor()
    sql = "select city, count(*) num from bs_51job where kw='{kw}' group by city order by num desc".format(kw=kw)
    cursor.execute(sql)
    data = cursor.fetchall()

    data_list = [list(z) for z in data]
    new_list = []

    conn.close()
    for data in data_list:
        if '异地' not in data[0]:
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

    return finally_list[:100]


def creat_lan_charts(data_list):
    page = Page()
    style = Style(
        title_color="#fff",
        title_pos="center",
        width=1200,
        height=600,
        background_color='#404a59'
    )

    chart = Geo("python", "python-city", **style.init_style)
    attr, value = chart.cast(data_list)
    chart.add("", attr, value, visual_range=[0, 200],
              visual_text_color="#fff", is_legend_show=False,
              symbol_size=15, is_visualmap=True,
              tooltip_formatter='{b}',
              label_emphasis_textsize=15,
              label_emphasis_pos='right')
    page.add(chart)

    chart = Geo("全国主要城市空气质量", "data from pm2.5", **style.init_style)
    attr, value = chart.cast(data_list)
    chart.add("", attr, value, type="heatmap", is_visualmap=True,
                visual_range=[0, 200], visual_text_color='#fff',
                is_legend_show=False)
    page.add(chart)
    return page

data_list = get_data('python')
t = creat_lan_charts(data_list)
t.render()
