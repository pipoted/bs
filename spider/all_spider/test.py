import requests
url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=03&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=22&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

print(len(requests.get(url).content.decode('gb2312')))
# print(requests.get(url).content.decode('gbk'))
