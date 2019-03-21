import time

from selenium import webdriver
from lxml import etree

browser = webdriver.Chrome()

url = 'https://www.lagou.com/jobs/5727314.html'

browser.get(url)
browser.implicitly_wait(50)
browser.find_element_by_class_name('name')
content = browser.page_source
tree = etree.HTML(content)
job = ''.join(tree.xpath('//span[@class="name"]/text()')).strip()
ps = tree.xpath('//dd[@class="job_request"]/p[1]')[0]
salary = ''.join(ps.xpath('./span[1]/text()')).strip()
area = ''.join(ps.xpath('./span[2]/text()')).replace('/', '').strip()
req = ''.join(ps.xpath('./span[3]/text()')).replace('/', '').strip()
edu = ''.join(ps.xpath('./span[4]/text()')).replace('/', '').strip()
types = ''.join(ps.xpath('./span[5]/text()')).strip()
print(types)
