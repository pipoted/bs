import random

from pyecharts import Bar, Page, Style
from app.charts.constants import WIDTH, HEIGHT


def create_charts():
    page = Page()

    style = Style(
        width=WIDTH, height=HEIGHT
    )

    attr = ["{}天".format(i) for i in range(30)]
    v1 = [random.randint(1, 30) for _ in range(30)]
    chart = Bar("柱状图-数据缩放(inside)", **style.init_style)
    chart.add("", attr, v1, is_datazoom_show=True, datazoom_type='inside',
              datazoom_range=[10, 60])
    page.add(chart)

    return page
