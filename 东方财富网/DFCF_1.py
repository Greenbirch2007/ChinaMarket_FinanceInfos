#! -*- coding:utf-8 -*-
import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()
# 把find_elements 改为　find_element
def get_first_page():

    url = 'http://data.eastmoney.com/bbsj/201906/yjyg.html'
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    return html





# 把首页和翻页处理？

def next_page():
    for i in range(1,16):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="PageCont"]/a[last()-1]').click()
        time.sleep(1)
        html = driver.page_source
        return html



def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    code = selector.xpath('//*[@id="dt_1"]/tbody/tr/td[2]/a/text()')
    name  =selector.xpath('//*[@id="dt_1"]/tbody/tr/td[3]/a/text()')
    description = selector.xpath('//*[@id="dt_1"]/tbody/tr/td[5]/text()')
    type = selector.xpath('//*[@id="dt_1"]/tbody/tr/td[9]/text()')
    Report_Time = selector.xpath('//*[@id="dt_1"]/tbody/tr/td[11]/text()')
    long_tuple = (i for i in zip(code, name,description, type, Report_Time))
    for i in long_tuple:
        big_list.append(i)
    return big_list


        # 存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                                 db='DFCF',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into DFCF_1 (code,name,description,type,Report_Time) values (%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass





if __name__ == '__main__':
        html = get_first_page()
        content = parse_html(html)
        print(content)
        # insertDB(content)
        # while True:
        #     html = next_page()
        #     content = parse_html(html)
        #     insertDB(content)
        #     print(datetime.datetime.now())
        #     time.sleep(5)


# code,name,description,type,Report_Time
# create table DFCF_1(
# id int not null primary key auto_increment,
# code varchar(10),
# name varchar(10),
# description text,
# type varchar(8),
# Report_Time varchar(10)
# ) engine=InnoDB  charset=utf8;

# drop table DFCF_1;

