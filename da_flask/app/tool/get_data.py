# -*- coding: <utf-8> -*-
# !/usr/bin/python
__author__ = 'xiao'
__date__ = '2019/4/16 11:27 PM'
from typing import List, Tuple

import pymysql


def clean_city_data(list_of_city: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    """
    处理初步从数据库中提取出的数据（其中包含着空格的数据）
    :return: 处理完成的列表
    """
    new_list = []  # 用来存放被初步处理的城市列表数据
    finally_list = []  # 用来存放最后返回的城市列表信息
    city_list = []  # 用来存放所有城市信息

    for data in list_of_city:  # 初步处理城市信息，去除城市信息中包含的空格
        new_list.append([data[0].replace(' ', ''), data[1]])

    # 将去除空格之后的城市信息中重复的进行合并，并将数量信息进行相加
    for num in range(len(list_of_city) - 1):
        city = new_list[num][0]
        if city not in city_list:
            city_list.append(city)
            city_num = new_list[num][1]
            for n in range(num + 1, len(new_list) - 2):
                if city in new_list[n][0]:
                    city_num += new_list[n][1]
            finally_list.append((city, city_num))

    return finally_list


class Data:
    def __init__(self):
        """
        初始化data类，初始化时创建数据库对象以及数据库游标对象，供提取信息时使用
        """
        print('初始化开始')
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='xzx199110',
            database='bs',
        )
        self.cursor = self.conn.cursor()
        self._list_of_lan = ['python', 'java', 'c语言', 'c＋＋', 'sql', 'go', 'php', 'c＃', 'JavaScript', 'perl', '.net',
                             'objective-c', 'MATLAB', 'R', 'assembly', 'swift', 'Delphi']
        self._list_of_job = ['前端', '后端', '软件开发', 'Android', 'ios', '测试', '运维', 'DBA', '算法', '架构', '运营', '大数据', '数据分析',
                             '机器学习', '游戏制作', '人工智能']
        self._city_name_list = []

    def __del__(self):
        """
        在删除对象的同时关闭数据对象
        """
        self.conn.close()

    def get_all_city_msg(self) -> List[Tuple[str, int]]:
        """
        提取所有城市包含的职位信息
        :return: 包含所有城市名称以及数量的元组的列表
        """
        sql = 'select city, count(*) num from bs_51job where not city="异地招聘" group by city order by num desc'
        self.cursor.execute(sql)
        _city_num_tuple = list(self.cursor.fetchall())

        return clean_city_data(list_of_city=_city_num_tuple)

    def _get_all_kw_msg(self) -> List[Tuple[str, int]]:
        """
        提取所有关键字信息
        :return: 包含所有关键字与数量信息的元组的列表
        """
        sql = 'select kw, count(*) num from bs_51job group by kw order by num desc'
        self.cursor.execute(sql)

        return list(self.cursor.fetchall())

    def get_the_lan_msg(self, kw_list: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        提取所有语言信息
        :param kw_list: 包含语言以及职位信息的列表
        :return: 返回只包含所有语言与数量信息的元组的列表
        """
        lan_list = []

        for kw in kw_list:
            if kw[0] in self._list_of_lan:
                lan_list.append(kw)

        return lan_list

    def get_the_job_msg(self, kw_list: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        提取所有职业信息
        :param kw_list: 包含语言以及职位信息的列表
        :return: 返回所有包含职业与数量信息的元组的列表
        """
        job_list = []

        for kw in kw_list:
            if kw[0] in self._list_of_job:
                job_list.append(kw)

        return job_list

    def get_all_lan_msg(self) -> List[Tuple[str, int]]:
        """
        提取所有语言信息
        """
        return self.get_the_lan_msg(kw_list=self._get_all_kw_msg())

    def get_all_job_msg(self) -> List[Tuple[str, int]]:
        """
        提取所有职位信息
        """
        return self.get_the_job_msg(kw_list=self._get_all_kw_msg())

    def get_the_city_msg(self, city_name: str) -> List[Tuple[str, int]]:
        """
        从数据库中提取指定城市中的职位与语言信息
        :param city_name: 目标城市
        :return: 语言信息与职位信息的元组
        """
        sql = 'select kw, count(*) num from bs_51job where city like "{city_name}%" group by kw order by num desc'.format(
            city_name=city_name
        )
        self.cursor.execute(sql)
        kw_list = list(self.cursor.fetchall())

        return kw_list

        # return (
        #     self.get_the_lan_msg(kw_list=kw_list),
        #     self.get_the_job_msg(kw_list=kw_list),
        # )

    def get_kw_msg_of_city(self, city_name: str) -> Tuple[list, list]:
        kw_list = self.get_the_city_msg(city_name=city_name)

        return (
            self.get_the_lan_msg(kw_list=kw_list),
            self.get_the_job_msg(kw_list=kw_list),
        )

    @staticmethod
    def _get_total(kw_list: List[Tuple[str, int]]) -> int:
        num = 0
        for tup in kw_list:
            num += tup[1]

        return num

    def _get_kw_num_of_the_city(self, city_name: str):
        """
        返回一个城市中语言总数与职位总数
        :param city_name: 目标城市名
        """
        lan_list, job_list = self.get_kw_msg_of_city(city_name=city_name)
        lan_num, job_num = self._get_total(lan_list), self._get_total(job_list)

        print('test', city_name)
        # result.append((city_name, lan_num, job_num))
        return city_name, lan_num, job_num

    def get_kw_num_of_all_city(self) -> List[Tuple[str, int, int]]:
        """
        返回所有城市的职位与语言数量
        """
        result_list = []

        for city in self.all_city_name()[:100]:
            result_list.append(self._get_kw_num_of_the_city(city_name=city))

        # gevent.joinall([
        #     gevent.spawn(self._get_kw_num_of_the_city, city, result_list) for city in self.all_city_name()[:100]
        # ])

        # with ThreadPoolExecutor(8) as executor:
        #     for city in self.all_city_name():
        #         executor.submit(self._get_kw_num_of_the_city, city, result_list)

        return result_list

    def get_the_kw_msg(self, lan_name: str) -> List[Tuple[str, int]]:
        """
        根据关键字返回其中包含的所有城市信息
        :param lan_name: 目标关键字
        :return: 所有城市信息
        """
        sql = 'select city, count(*) num from bs_51job where kw="{lan_name}" and not city="异地招聘" group by city order by num desc'.format(
            lan_name=lan_name
        )
        self.cursor.execute(sql)

        return clean_city_data(list(self.cursor.fetchall()))

    def all_city_name(self):
        return [city[0] for city in self.get_all_city_msg()]

    def top5_city_name(self) -> List[str]:
        """
        查询职位数量前五的城市
        :return: 包含城市名称的列表
        """
        return [data[0] for data in self.get_all_city_msg()[:5]]

    def top5_lan_name(self) -> List[str]:
        """
        查询数量排名前五的语言
        :return: 包含语言名称的列表
        """
        return [data[0] for data in self.get_all_lan_msg()[:5]]

    def top5_job_name(self) -> List[str]:
        """
        查询熟练排名前五的职位
        :return: 包含职位名称的列表
        """
        return [data[0] for data in self.get_all_job_msg()[:5]]
