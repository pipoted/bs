#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from urllib import request
from selenium import webdriver
from selenium import webdriver

url = 'https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId=489&salary=1,1000&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3&=1&_v=0.54277500&x-zp-page-request-id=20aa3cf26b9d4d05b4aaafe175de0c6d-1552385870753-809381'
# url = 'https://www.zhipin.com/c100010000/s_306/?query=python&period=1&page=2&ka=page-2'
# url = 'http://httpbin.org/ip'
# url = 'https://ip.cn/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Cookie': 'sts_deviceid=166ed6e87ff274-09a26b86e44dbc-1e396652-1296000-166ed6e880172; __xsptplus30=30.1.1541581736.1541581736.1%231%7CbaiduPC%7CCPC%7Cpp%7C8804380%7Cpp%23%23BvCtoqpdu9sv5gnKORbH8IEQdyJrPnJ0%23; _jzqa=1.2946990015629254700.1541581736.1541581736.1541581736.1; _jzqy=1.1541581736.1541581736.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94.-; zg_did=%7B%22did%22%3A%20%22166ed6f4b801256-09b69a1809a3de-1e396652-13c680-166ed6f4b8127b%22%7D; zg_08c5bcee6e9a4c0594a5d34b79b9622a=%7B%22sid%22%3A%201541581785992%2C%22updated%22%3A%201541581845832%2C%22info%22%3A%201541581785994%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22i.zhaopin.com%22%7D; adfbid2=0; acw_tc=2760828715512837927115400eda8e860c12bcf9b5c4b39064b6e0d1b493ef; dywea=95841923.769450324944796200.1541581736.1541581736.1551283793.2; dywez=95841923.1551283793.2.2.dywecsr=cn.bing.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/; campusOperateJobUserInfo=419cfff7-2b36-4566-a1ca-4aaab7f9b6ef; urlfrom=121122526; urlfrom2=121122526; adfcid=u243985234.c2327960903.g3721973691.k20618608849.pq; adfcid2=u243985234.c2327960903.g3721973691.k20618608849.pq; adfbid=0; C_PC_TEST=cddb158b-5128-4fb9-b2e6-da54cb1fbc58; sts_sg=1; sts_chnlsid=121122526; zp_src_url=https%3A%2F%2Fcn.bing.com%2F; jobRiskWarning=true; ZP_OLD_FLAG=false; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221011635495%22%2C%22%24device_id%22%3A%22166ed6e86ca51b-0d9465471abddf-1e396652-1296000-166ed6e86cd415%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%2C%22%24latest_referrer_host%22%3A%22cn.bing.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_utm_source%22%3A%22360PC%22%2C%22%24latest_utm_medium%22%3A%22CPC%22%2C%22%24latest_utm_campaign%22%3A%22pp%22%2C%22%24latest_utm_content%22%3A%22qg%22%2C%22%24latest_utm_term%22%3A%2210920959%22%7D%2C%22first_id%22%3A%22166ed6e86ca51b-0d9465471abddf-1e396652-1296000-166ed6e86cd415%22%7D; LastCity=%E5%85%A8%E5%9B%BD; LastCity%5Fid=489; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1552372542,1552372885,1552385786,1552385872; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1552385872; ZL_REPORT_GLOBAL={%22sou%22:{%22actionid%22:%226f15c4a5-eda0-45aa-8515-f32a9d347928-sou%22%2C%22funczone%22:%22smart_matching%22}}; acw_sc__v2=5c89b15ffb078061e702c6f0bcfb9e84801aa9d9',
}
proxies = {
    'http': 'http://125.40.109.154:31610',
    'https': 'https://221.206.100.133:34073',
}

# print(requests.get(url, headers=headers, proxies=proxies, verify=False).content.decode())
# 106.39.149.84

browser = webdriver.Chrome()
browser.get(url)

print(browser.page_source)
browser.close()
