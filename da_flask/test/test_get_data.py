# !/usr/bin/python
# -*- coding: <utf-8> -*-
__author__ = 'xiao'
__date__ = '2019/4/16 11:53 PM'

from app.tool.get_data import Data

data = Data()

# city_list = data._get_all_city_msg()
# kw_list = data._get_all_kw_msg()
# print(kw_list)

# lan_list = data._get_all_lan_msg()
# print(lan_list)

# job_list = data._get_all_job_msg()
# print(job_list)

# lan_list, job_list = data.get_the_city_msg('上海')
# print(lan_list)
# print(job_list)

# city_list = data.get_the_kw_msg('ios')
# print(city_list)

# city_list = data.top5_city_name()
# print(city_list)

# lan_list = data.top5_job_name()
# print(lan_list)

city_list = data.all_city_name()
print(city_list)