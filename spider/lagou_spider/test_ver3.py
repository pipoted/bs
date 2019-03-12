#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

url = 'https://www.lagou.com/jobs/positionAjax.json'
data = {
    'first': 'false',
    'pn': '2',
    'kd': 'python爬虫',
}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '44',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'user_trace_token=20180819192158-2fac8a62-adee-477a-a93a-b9240417b9c4; _ga=GA1.2.1296471722.1534677721; LGUID=20180819192200-174df15d-a3a2-11e8-92e4-525400f775ce; index_location_city=%E5%8C%97%E4%BA%AC; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221693559bf0aa93-0f0ac32e50e7d2-36657105-1296000-1693559bf0b4db%22%2C%22%24device_id%22%3A%221693559bf0aa93-0f0ac32e50e7d2-36657105-1296000-1693559bf0b4db%22%7D; LG_LOGIN_USER_ID=f525badde3474a05bcd2cdc5cbdd1b15baa9c8da8403963b0296be73d45e9106; JSESSIONID=ABAAABAAADEAAFI6F7D16118E4C3F4871BA0EFE4334FF0A; _gid=GA1.2.1524731431.1552287450; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551283152,1551283516,1552287450; TG-TRACK-CODE=search_code; _gat=1; LGSID=20190312033310-812b0d15-4434-11e9-b629-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; SEARCH_ID=334679b65f6b4fb4b0400945dfe89742; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552332833; LGRID=20190312033353-9a69f644-4434-11e9-9428-5254005c3644',
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?px=default&city=%E5%85%A8%E5%9B%BD',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': 'None',
    'X-Requested-With': 'XMLHttpRequest',
}
resp = requests.get(url=url, params=data)
print(resp.content.decode())
