# !/usr/bin/python
# -*- coding: <utf-8> -*-
__author__ = 'xiao'
__date__ = '2019/4/17 1:29 AM'

from pyecharts import (
    Pie, Bar, Line, WordCloud, Map, Geo
)
from pyecharts.charts import (
    bar, map, pie, wordcloud, line, geo
)
from app.charts.constants import WIDTH, HEIGHT
from pyecharts import Style
from typing import List, Tuple


def bar_ssdd(attr_v1_v2: List[Tuple[str, int, int]], chart_name: str, v1_name: str, v2_name: str) -> bar.Bar:
    """
    生成一个数据堆叠的图表
    :param attr_v1_v2: 包含想要显示的数据列表
    :param chart_name: 图表名
    :param v1_name: 数据一名
    :param v2_name: 数据二名
    """
    style = Style(
        width=WIDTH, height=HEIGHT
    )

    attr = [a[0] for a in attr_v1_v2]
    v1 = [v[1] for v in attr_v1_v2]
    v2 = [v[2] for v in attr_v1_v2]
    chart = Bar(chart_name, **style.init_style)
    chart.add(v1_name, attr, v1, is_stack=True)
    chart.add(v2_name, attr, v2, is_stack=True, is_more_utils=True)

    return chart


def bar_sssf(attr_v1: List[Tuple[str, int]], chart_name: str, v1_name: str) -> bar.Bar:
    """
    生成柱状图-数据缩放图表
    :param attr_v1: 主要数据
    :param chart_name: 图表名
    :param v1_name: 数据一名
    """
    style = Style(
        width=WIDTH, height=HEIGHT
    )
    attr = [a[0] for a in attr_v1]
    v1 = [v[1] for v in attr_v1]
    chart = Bar(chart_name, **style.init_style)
    chart.add(v1_name, attr, v1, is_datazoom_show=True, datazoom_type='both',
              datazoom_range=[0, 20])

    return chart


def line_ssdd(attr_v1_v2: List[Tuple[str, int, int]], chart_name: str, v1_name: str, v2_name: str) -> line.Line:
    """
    生成一个折线图-数据堆叠图
    :param attr_v1_v2: 包含想要显示的数据列表
    :param chart_name: 图表名
    :param v1_name: 数据一名
    :param v2_name: 数据二名
    """
    style = Style(
        width=WIDTH, height=HEIGHT
    )
    attr = [a[0] for a in attr_v1_v2]
    v1 = [v[1] for v in attr_v1_v2]
    v2 = [v[2] for v in attr_v1_v2]
    # chart = Line(chart_name, **style.init_style)
    # chart.add(v1_name, attr, v1, is_label_show=True, is_smooth=True)
    # chart.add(v2_name, attr, v2, is_label_show=True, is_smooth=True)

    chart = Line(chart_name, **style.init_style)
    chart.add(v1_name, attr, v1, mark_point=["average"])
    chart.add(v2_name, attr, v2, is_smooth=True, mark_line=["max", "average"], is_more_utils=True)

    return chart


def geo_qgtd(attr_v1: List[Tuple[str, int]], chart_name: str, v1_name: str) -> geo.Geo:
    """
    生成全国地图-数据通道图
    :param attr_v1: 主要数据
    :param chart_name: 图表名
    :param v1_name: 数据一名
    """
    style = Style(
        title_color="#fff",
        title_pos="center",
        width=900,
        height=600,
        background_color='#404a59'
    )
    # chart = Map(chart_name, **style.init_style)
    # chart.add(v1_name, attr, value, maptype='china', is_visualmap=True,
    #           visual_text_color='#000')
    chart = Geo(chart_name, "", **style.init_style)
    attr, value = chart.cast(attr_v1)
    chart.add(v1_name, attr, value, visual_range=[0, 70000], visual_text_color="#fff", is_legend_show=False,
              symbol_size=15, is_visualmap=True, tooltip_formatter='{b}', label_emphasis_textsize=15,
              label_emphasis_pos='right', type='effectScatter')

    return chart


def map_qgtd(attr_v1: List[Tuple[str, int]], chart_name: str, v1_name: str) -> map.Map:
    style = Style(
        width=WIDTH, height=HEIGHT
    )
    chart = Map(chart_name, **style.init_style)
    attr, value = chart.cast(attr_v1)
    chart.add(v1_name, attr, value, maptype='china', is_visualmap=True,
              visual_text_color='#000')

    return chart


def pie_yht(attr_v1: List[Tuple[str, int]], chart_name: str, v1_name: str) -> pie.Pie:
    """
    生成饼图-圆环图
    :param attr_v1: 主要数据
    :param chart_name: 图表名
    :param v1_name: 数据一名
    """
    style = Style(
        width=WIDTH, height=HEIGHT
    )
    attr = [a[0] for a in attr_v1]
    v1 = [v[1] for v in attr_v1]
    chart = Pie(chart_name, title_pos='center', **style.init_style)
    chart.add(v1_name, attr, v1, radius=[40, 75], label_text_color=None,
              is_label_show=True, legend_orient='vertical', legend_pos='left')

    return chart


def wordcloud_zdy(attr_v1: List[Tuple[str, int]], chart_name: str, v1_name: str) -> wordcloud.WordCloud:
    """
    生成词云图
    :param attr_v1: 主要数据
    :param chart_name: 图表名
    :param v1_name: 数据一名
    """
    style = Style(
        width=1100, height=600
    )
    name = [n[0] for n in attr_v1]
    value = [v[1] for v in attr_v1]
    chart = WordCloud(chart_name, **style.init_style)
    chart.add(v1_name, name, value, word_size_range=[30, 100], shape='diamond')

    return chart
