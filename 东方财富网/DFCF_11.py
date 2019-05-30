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

    url = 'http://data.eastmoney.com/gphg/'
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    return html





# 把首页和翻页处理？

def next_page():
    for i in range(1,18):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="PageCont"]/a[last()-1]').click()
        time.sleep(1)
        html = driver.page_source
        return html


# 正则
def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    patt = re.compile(
        '<td><a href=".*?">(.*?)</a></td><td><a href=".*?">(.*?)</a></td><td><a class="red" href=".*?">详细</a></td><td><span>(.*?)</span></td><td><span>(.*?)</span></td><td><span>(.*?)</span></td><td><span>(.*?)</span></td><td><span>(.*?)</span></td><td><span title=".*?">(.*?)</span></td><td><span>(.*?)</span></td><td><span>(.*?)</span></td><td><span>(.*?)</span></td><td><span>(.*?)</span></td><td><span title=".*?">(.*?)</span></td></tr>',
        re.S)
    items = re.findall(patt, html)
    for item in items:
        big_list.append(item)
    return big_list


        # 存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                                 db='DFCF',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into DFCF_11 (code,name,last_price,plan_price,plan_SNums,plan_Percent,plan_Money,plan_StartTime,plan_procession,hasDone_price,hasDone_Nums,hasDone_Money,last_ReportTime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass


#

if __name__ == '__main__':
        html = get_first_page()
        content = parse_html(html)
        insertDB(content)
        while True:
            html = next_page()
            content = parse_html(html)
            insertDB(content)
            print(datetime.datetime.now())
            time.sleep(5)


# code,name,last_price,plan_price,plan_SNums,plan_Percent,plan_Money,plan_StartTime,plan_procession,hasDone_price,hasDone_Nums,hasDone_Money,last_ReportTime
# create table DFCF_11(
# id int not null primary key auto_increment,
# code varchar(10),
# name varchar(10),
# last_price varchar(100),
# plan_price varchar(100),
# plan_SNums varchar(100),
# plan_Percent varchar(50),
# plan_Money varchar(100),
# plan_StartTime varchar(100),
# plan_procession varchar(50),
# hasDone_price varchar(100),
# hasDone_Nums varchar(100),
# hasDone_Money varchar(100),
# last_ReportTime varchar(10)
# ) engine=InnoDB  charset=utf8;

# drop table DFCF_11;

