# !/usr/bin/python
# -*- coding: <utf-8> -*-

import requests
import json

url = 'https://fe-api.zhaopin.com/c/i/sou?start=90&pageSize=90&cityId=489&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3&=0&rt=cdebee05f68b46ad9b2826ad59465995&_v=0.67395132&x-zp-page-request-id=4e016822e03b42238ccdde80f80db89f-1554534268499-442740'

content = requests.get(url).content.decode()
data = json.loads(content)['data']['results']
print(data)
print(len(data))
