from selenium import webdriver
from lxml import etree
import pymysql

url = 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?px=default&city=%E5%85%A8%E5%9B%BD#filterBox'

browser = webdriver.Chrome()
browser.get(url)

content = browser.page_source
tree = etree.HTML(content)
browser.close()

lis = tree.xpath('//div[@class="s_position_list "]/ul/li')
meg_list = []
for li in lis:
    job = li.xpath('.//a[@class="position_link"]/h3/text()')[0].strip()
    money = li.xpath('.//span[@class="money"]/text()')[0].strip()
    need = li.xpath('.//div[@class="li_b_l"]/text()')[2].strip()
    company = li.xpath('.//div[@class="company_name"]/a/text()')
    meg_dict = {
        'job': job,
        'money': money,
        'need': need,
        'company': company,
    }
    meg_list.append(meg_dict)


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='xzx199110',
    database='bs',
    port=3306,
)
cursor = conn.cursor()
sql = """ insert into lagou_test (job, money, need, company) values (%s, %s, %s, %s);
"""

for item in meg_list:
    cursor.execute(sql, (item['job'], item['money'],
                         item['need'], item['company']))
    conn.commit()


conn.close()
