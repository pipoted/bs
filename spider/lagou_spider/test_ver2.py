from selenium import webdriver


url = 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?px=default&city=%E5%85%A8%E5%9B%BD#filterBox'

browser = webdriver.Chrome()
browser.get(url)

try:
    browser.find_element_by_class_name('pager_next pager_next_disabled').click()
except:
    print('false')
finally:
    browser.close()
