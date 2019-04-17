# !/usr/bin/python
# -*- coding: <utf-8> -*-
__author__ = 'xiao'
__date__ = '2019/4/17 3:02 AM'

from app.tool import creat_chart


test = creat_chart.line_ssdd([('test', 1, 10)], 'test', 'tst', 'test')
test.render()

