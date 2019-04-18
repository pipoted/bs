from flask import render_template, request, redirect, url_for, abort
from app.tool.get_data import Data
from app.tool.creat_chart import (
    pie_yht, bar_sssf, bar_ssdd, line_ssdd, geo_qgtd, wordcloud_zdy, map_qgtd
)
from pyecharts import Page

from . import app

# 对一些数据进行预处理
DATA = Data()
KW_NUM_OF_ALL_CITY_LIST = DATA.get_kw_num_of_all_city()
CITY_NUM_LIST = DATA.get_all_city_msg()
LAN_NUM_LIST = DATA.get_all_lan_msg()
JOB_NUM_LIST = DATA.get_all_job_msg()
CITY_NAME_LIST = DATA.all_city_name()
LAN_NAME_LIST = DATA.all_lan_list()
JOB_NAME_LIST = DATA.all_job_list()
ALL_NUM = DATA.get_all_num()


@app.route("/")
def home():
    """
    主页信息
    """
    # 将要显示的数据
    print('test')
    city_num_list = CITY_NUM_LIST[:100]
    kw_num_city_list = KW_NUM_OF_ALL_CITY_LIST[:100]
    lan_num_list = LAN_NUM_LIST
    job_num_list = JOB_NUM_LIST
    all_num = ALL_NUM

    # 生成相应的图表
    top_10_city_page = Page()
    top_10_city_page.add(bar_ssdd(
        attr_v1_v2=kw_num_city_list[:10],
        chart_name='前十城市中语言数与职位数对比-折线图',
        v1_name='语言数量',
        v2_name='职位数量',
    ))

    top_10_city_map_page = Page()
    top_10_city_map_page.add(
        geo_qgtd(attr_v1=city_num_list[:10], chart_name='前十城市地理位置', v1_name='城市')
    )

    top_100_city_page = Page()
    top_100_city_page.add(
        bar_sssf(attr_v1=city_num_list, chart_name='前百城市职位数量-柱状图', v1_name='职位数')
    )
    top_100_city_map_page = Page()
    top_100_city_map_page.add(
        geo_qgtd(attr_v1=city_num_list[:100], chart_name='前百城市地理位置', v1_name='城市')
    )

    lan_page = Page()
    lan_page.add(
        pie_yht(attr_v1=lan_num_list, chart_name='各种语言占总数比值-饼图', v1_name='语言')
    )

    job_page = Page()
    job_page.add(
        pie_yht(attr_v1=job_num_list, chart_name='各种职位占总数比值-饼图', v1_name='职位')
    )

    return render_template(
        'index.html',
        title='首页',
        all_num=all_num,
        top5_city=DATA.top5_city_name(),
        top5_lan=DATA.top5_lan_name(),
        top5_job=DATA.top5_job_name(),
        top_10_city=top_10_city_page.render_embed(),
        top_10_city_map_page=top_10_city_map_page.render_embed(),
        top_100_city_page=top_100_city_page.render_embed(),
        top_100_city_map_page=top_100_city_map_page.render_embed(),
        lan_page=lan_page.render_embed(),
        job_page=job_page.render_embed(),
        script_list=top_10_city_page.get_js_dependencies()
                    + top_100_city_page.get_js_dependencies()
                    + lan_page.get_js_dependencies()
                    + job_page.get_js_dependencies()
                    + top_10_city_map_page.get_js_dependencies()
                    + top_100_city_map_page.get_js_dependencies(),
    )


@app.route('/city<city>')
def city_page(city):
    # 需要处理的数据
    lan_list, job_list = DATA.get_kw_msg_of_city(city_name=city)
    kw_list = DATA.get_the_city_msg(city_name=city)
    kw_num = DATA.get_kw_num(city=city)
    lan_num, job_num = DATA.get_lan_job_num(city=city)

    # 生成数据图表
    kw_bar_page = Page().add(
        bar_sssf(attr_v1=kw_list, chart_name=city + '各种职位总览-柱状图', v1_name='数量')
    )

    ## 对语言的分析柱状图与饼图
    lan_bar_page = Page().add(
        bar_sssf(attr_v1=lan_list, chart_name=city + '各语言数量-柱状图', v1_name='语言')
    )
    lan_pie_page = Page().add(
        pie_yht(attr_v1=lan_list, chart_name='每种语言占总数占比-饼状图', v1_name='语言')
    )

    ## 对职位的分析柱状图与饼图
    job_bar_page = Page().add(
        bar_sssf(attr_v1=job_list, chart_name=city + '各职位数量-柱状图', v1_name='职位')
    )
    job_pie_page = Page().add(
        pie_yht(attr_v1=job_list, chart_name='每种职位占总数占比-饼状图', v1_name='职位')
    )

    return render_template(
        'city.html',
        title=city,
        kw_list=kw_list,
        lan_num=lan_num,
        job_num=job_num,
        top5_city=DATA.top5_city_name(),
        top5_lan=DATA.top5_lan_name(),
        top5_job=DATA.top5_job_name(),
        kw_bar_page=kw_bar_page.render_embed(),
        lan_bar_page=lan_bar_page.render_embed(),
        lan_pie_page=lan_pie_page.render_embed(),
        job_bar_page=job_bar_page.render_embed(),
        job_pie_page=job_pie_page.render_embed(),
        script_list=kw_bar_page.get_js_dependencies()
                    + lan_bar_page.get_js_dependencies()
                    + lan_pie_page.get_js_dependencies()
                    + job_bar_page.get_js_dependencies()
                    + job_pie_page.get_js_dependencies(),
    )


@app.route('/lan<lan>')
def lan_page(lan):
    # 需要处理的数据
    city_num_list = DATA.get_the_kw_msg(lan_name=lan)

    # 生成图表
    ## 生成地理图
    city_geo_page = Page().add(
        pie_yht(attr_v1=city_num_list[:20], chart_name=lan + '每个城市占总的比重', v1_name='城市')
    )

    ## 生成柱状图
    city_bar_page = Page().add(
        bar_sssf(attr_v1=city_num_list[:100], chart_name=lan + '每个城市中该职位数量', v1_name='城市')
    )
    return render_template(
        'lan.html',
        title=lan,
        top5_city=DATA.top5_city_name(),
        top5_lan=DATA.top5_lan_name(),
        top5_job=DATA.top5_job_name(),
        city_geo_page=city_geo_page.render_embed(),
        city_bar_page=city_bar_page.render_embed(),
        script_list=city_geo_page.get_js_dependencies()
                    + city_bar_page.get_js_dependencies(),
    )


@app.route('/job<job>')
def job_page(job):
    # 需要处理的数据
    city_num_list = DATA.get_the_kw_msg(lan_name=job)

    # 生成图表
    ## 饼图
    city_geo_page = Page().add(
        pie_yht(attr_v1=city_num_list[:20], chart_name=job + '前二十个城市各自占的比重', v1_name='城市')
    )

    ## 生成柱状图
    city_bar_page = Page().add(
        bar_sssf(attr_v1=city_num_list[:100], chart_name=job + '每个城市中该职位数量', v1_name='城市')
    )
    return render_template(
        'lan.html',
        title=job,
        top5_city=DATA.top5_city_name(),
        top5_lan=DATA.top5_lan_name(),
        top5_job=DATA.top5_job_name(),
        city_geo_page=city_geo_page.render_embed(),
        city_bar_page=city_bar_page.render_embed(),
        script_list=city_geo_page.get_js_dependencies()
                    + city_bar_page.get_js_dependencies(),
    )


@app.route('/search', methods=['POST'])
def search():
    search = request.form['search']  # type: str
    if search in CITY_NAME_LIST:
        return redirect(url_for('city_page', city=search))
    elif search.lower() in LAN_NAME_LIST:
        if '+' in search:
            search.replace('+', '＋')
        if '#' in search:
            search.replace('#', '＃')
        return redirect(url_for('lan_page', lan=search))
    elif search in JOB_NAME_LIST:
        return redirect(url_for('job_page', job=search))
    else:
        abort(404)

    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
