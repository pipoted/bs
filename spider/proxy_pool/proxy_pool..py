# coding=utf-8
__author__ = 'xiao'
__date__ = '2019/3/16 9:19 AM'

from gevent import monkey

monkey.patch_all()
import requests
import re
import time
from lxml import etree
from gevent import queue, pool


class Dynamic_Proxy_Pool:
    """
    xici 代理动态代理池
    """

    def __init__(self):
        self.proxy_queue = queue.Queue(maxsize=100)
        self.pool = pool.Pool(3)

    def __next__(self):
        self.return_useful_proxy()

    @staticmethod
    def ip_test(proxies: dict):
        url = 'http://icanhazip.com/'
        requests.adapters.DEFAULT_RETRIES = 3
        try:
            resp = requests.get(url, timeout=2, proxies=proxies)
            print(resp.text)
        except BaseException:
            return False

    def get_proxy_dict(self, url):
        import time
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Cookie': 'free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWY2M2JmODhlNDNlN2FlYTQxM2RjMGUyNGJmMzcwMTY4BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUo5SVF1VmxncTlrWUwydzhadFN3NURtNUpBS2syQXlGQjZkcm01S2VVM0E9BjsARg%3D%3D--da2ef70cbed6026258a49157ba64cd21d8d06c92; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1551063767,1552289412,1552645377; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1552699388',
        }

        resp = requests.get(url, headers=headers)
        status = resp.status_code
        if status != 200:
            time.sleep(10)
            self.get_proxy_dict(url)
        content = resp.content.decode()
        tree = etree.HTML(content)

        trs = tree.xpath('//table[@id="ip_list"]//tr')[1:]
        print(len(trs))
        for tr in trs:
            ip = tr.xpath('.//td[2]/text()')[0].strip()
            port = tr.xpath('.//td[3]/text()')[0].strip()
            types = tr.xpath('.//td[6]/text()')[0].strip().lower()
            speed = tr.xpath('.//td[7]/div/div/@style')[0]
            speed = int(re.findall('.*?(\d+)%', speed)[0])
            time_temp = tr.xpath('.//td[8]/div/div/@style')[0]
            time = int(re.findall('.*?(\d+)%', time_temp)[0])
            if speed >= 95 and time >= 95 and ('HTTP' in types or 'HTTPS' in types):
                if not self.proxy_queue.full():
                    proxy = '%s://%s:%s' % (types, ip, port)
                    self.proxy_queue.put(proxy)
                else:
                    raise OverflowError

    def loop_spider_proxy(self):
        page = 1
        while True:
            url = 'https://www.xicidaili.com/nn/%s' % str(page)
            print('start', url)
            try:
                self.get_proxy_dict(url)
                page += 1
                time.sleep(10)
            except OverflowError:
                return

    def return_useful_proxy(self):
        if self.proxy_queue.qsize() > 90:
            proxy = self.proxy_queue.get()
            proxy_dict = {
                'http': proxy,
                'https': proxy,
            }
            if not self.ip_test(proxy_dict):
                return proxy_dict
        else:
            self.proxy_queue.__init__(100)
            self.loop_spider_proxy()
            self.return_useful_proxy()

    useful_proxy = return_useful_proxy()


if __name__ == '__main__':
    proxy = Dynamic_Proxy_Pool()
    print(proxy.useful_proxy)
