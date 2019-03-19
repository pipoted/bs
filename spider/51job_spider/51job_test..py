# coding=utf-8
__author__ = 'xiao'
__date__ = '2019/3/19 10:49 AM'

import requests

url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,%2B,2,5.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=21&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

content = requests.get(url).content.decode(encoding='gbk')
