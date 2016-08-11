# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 17:06:46 2016

@author: tristan
"""
'''
大概的程序框架:
    1. 读取保存好的csv文件(pandas)
    2. 根据colums(brand_name)遍历品牌
    3.      根据index(date)遍历日期
    4.      获取url,日期
    5.      以日期为名字, 路径为brand_name/small_img, 下载图片
'''

import time
import random
import urllib2
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

print time.strftime('%H:%M:%S', time.localtime())

import pandas as pd


class save_img:
    def __init__(self, wrong_record=[],
                 img_path='img_path',
                 csv_path='csv_path',
                 test_xlsx='xls_path'):
        self.wrong_record = wrong_record
        self.img_path = img_path
        self.csv_path = csv_path
        self.test_xlsx = test_xlsx
        self.csv_df = pd.read_csv(self.csv_path)
        self.connect_time = 0

    def save_each_long_img(self, headers, imgurl, brand_name, img_name):
        # 异常处理, 如果超时, 重试一次, 继续超时, 直接跳过
        try:
            request = urllib2.Request(imgurl, headers=headers)
            img = urllib2.urlopen(request, timeout=8)
        except:
            request = urllib2.Request(imgurl, headers=headers)
            img = urllib2.urlopen(request, timeout=8)

        with open(''.join([self.img_path, brand_name, '/long_img/', img_name, '.jpg']), 'wb') as localFile:  # 图片保存的地址
            localFile.write(img.read())
        self.sleep_random()
        img.close()
        

    def open_browser(self):
        browser = webdriver.Firefox()
        # browser = webdriver.Chrome('/Users/macbookpro/Desktop/python/crawler/chromedriver 2') # for Chrome
        browser.get('domain')
        return browser

    def loginToWeb(self, browser):
        wait = WebDriverWait(browser, 20)
        def input_info():
            user_name = browser.find_element_by_id('email')
            user_name.send_keys('username')
            time.sleep(1)
            password = browser.find_element_by_id('password')
            password.send_keys('password')
            time.sleep(1)
            login_button = browser.find_element_by_id('login_acc')
            login_button.click()
            wait.until(lambda browser: browser.find_element_by_link_text('My Account'))
            return browser.get_cookie('.AspNet.ApplicationCookie')['value']

        try:
            log_out_button = browser.find_element_by_link_text('Log out')
            log_out_button.click()
            wait.until(lambda browser: browser.find_element_by_link_text('Log In'))
            show_log_form = browser.find_element_by_link_text('Log In')
            show_log_form.click()
            time.sleep(2)
            return input_info()
                       
        except:
            show_log_form = browser.find_element_by_link_text('Log In')
            show_log_form.click()
            time.sleep(2)
            return input_info()

    def count_time(self, begin_time):
        now_time = time.time()
        run_time = now_time - begin_time
        return now_time, run_time

    def get_headers(self, cookies=''):
        user_agent_list = ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
                           'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                           'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
                           'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', ]
        user_agent = random.choice(user_agent_list)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Cookie': '{cookie}'.format(cookie=cookies),
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': '{user_agent}'.format(user_agent=user_agent)
        }
        return headers

    def travel_csv(self):
        csv_df = self.csv_df  # 打开保存图片url的csv文件
        test_xlsx = pd.read_excel(self.test_xlsx)  # 用于记录已经下载过的图片的文件
        browser = self.open_browser()  # 打开浏览器
        screen_cookies = '.AspNet.ApplicationCookie={get_cookie}'.format(
            get_cookie=self.loginToWeb(browser))  # 获取cookies
        headers = self.get_headers(cookies=screen_cookies)  # 获取headers,包含cookies的
        begin_time = time.time()

        for i in xrange(1, len(csv_df.columns)):  # 因为columns真实是从1开始的, len-1结束的
            print i, 'Begin to download img: {brand_name}'.format(brand_name=csv_df.columns[i])
            for j in xrange(len(csv_df.index)):

                if pd.isnull(csv_df.ix[j, i]) or test_xlsx.ix[j, i] == 1:  # 空的或者已经下载过了的跳过
                    if j % 100 == 0:
                        print '   ', j
                    continue


                else:
                    now_time, run_time, = self.count_time(begin_time)
                    if run_time > 7200:     # 因为网站cookies life_time比较短, 所以设置2个小时的登录间隔
                        try:
                            screen_cookies = '.AspNet.ApplicationCookie={get_cookie}'.format(
                                get_cookie=self.loginToWeb(browser))  # 获取cookies
                            headers = self.get_headers(cookies=screen_cookies)
                            begin_time = now_time
                            self.connect_time = 0
                        except:
                            self.connect_time += 1

                    if self.connect_time > 2:           # 设置失败登录次数, 如果失败超过三次, 那么意味着cookies可能会过期, 所以返回错误(防止长时间断网)
                        raise "connect error"

                    try:
                        self.save_each_long_img(headers=headers,
                                                imgurl=csv_df.ix[j, i],
                                                brand_name=csv_df.columns[i],
                                                img_name=csv_df.ix[:, 0][j])
                        test_xlsx.ix[j, i] = 1
                    except:
                        continue

                    # 记录已经下载过的 且每下载100张图片保存一次.

                    if j % 30 == 0:         # 用于记录已经下载过的图片
                        test_xlsx.to_excel(self.test_xlsx)
                    if j % 100 == 0:        # 只是给一个可视化的过程输出
                        test_xlsx.to_excel(self.test_xlsx)
                        print time.strftime('%H:%M:%S', time.localtime()), ' ', j

    def sleep_random(self):
        if time.localtime().tm_hour > 22 or time.localtime().tm_hour < 9:       # 美国的网站, 所以设置晚上低速下载
            x, y = random.uniform(3.0, 4.2), random.uniform(4.8, 6.0)
        else:
            x, y = random.uniform(0.2, 0.3), random.uniform(0.4, 0.5)

        return time.sleep(random.uniform(x, y)
                          if random.randint(1, 1000) > 2
                          else random.uniform(30.213, 40.034))


def main():
    test_save_img = save_img()
    test_save_img.travel_csv()


if __name__ == "__main__":
    main()

