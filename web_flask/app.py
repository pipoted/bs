#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
from flask import Flask, render_template
from pyecharts import Geo, Style, Page

app = Flask(__name__)


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

    for data in data_list:
        if '异地' not in data[0]:
            new_list.append([data[0].replace(' ', ''), data[1]])

    finally_list = []
    city_list = []
    for num in range(len(data) - 1):
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

    chart = Geo("全国主要城市空气质量", "data from pm2.5", **style.init_style)
    attr, value = chart.cast(data_list)
    chart.add("", attr, value, type="heatmap", is_visualmap=True,
              visual_range=[0, 200], visual_text_color='#fff',
              is_legend_show=False)
    page.add(chart)

    return page


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/city/<city_name>')
def city_page(city_name):
    desc = 'test' + city_name
    return render_template('city_page.html', city_name=city_name, desc=desc)


@app.route('/lan/<lan_name>')
def lan_page(lan_name):
    desc = 'test' + lan_name
    data_list = get_data(lan_name)
    lan_chart = creat_lan_charts(data_list)
    return render_template('lan_page.html', lan_name=lan_name, desc=desc, lan_chart=lan_chart.render_embed(),
                           script_list=lan_chart.get_js_dependencies())


if __name__ == '__main__':
    app.run()
