#-- coding=utf-8 --#
'''  Tristan SHi '''

import random
import time
import datetime
from pyquery import PyQuery as pq
import pandas as pd

print time.strftime('%H:%M:%S', time.localtime())

class down_img_url:
    def __init__(self,
                 down_record={}, down_record_2={}, down_quantity={},
                 domain='domain',
                 brand_done=[], brand_count=-1,
                 excel_loc = 'path'):
        self.down_record = down_record
        self.down_record_2 = down_record_2
        self.down_quantity = down_quantity
        self.domain = domain
        self.brand_done = brand_done
        self.brand_count = brand_count
        self.excel_loc = excel_loc


    def get_img_name(self, info, index):
        img_info = info('h3.page-title')('span')[index].text
        strpDate = time.strptime(img_info, '%m/%d/%Y')
        img_name = ''.join([str(strpDate.tm_year), '-', str(strpDate.tm_mon), '-', str(strpDate.tm_mday)])
        return img_name


    def get_now_date(self):
        # 获得现在的年, 月, 日
        year_now,month_now, days_now  = int(time.strftime('%Y', time.localtime(time.time()))),\
                                        int(time.strftime('%m', time.localtime(time.time()))),\
                                        int(time.strftime('%d', time.localtime(time.time())))

        date_now = datetime.date(year_now, month_now, days_now)
        date_begain = date_now - datetime.timedelta(1)  # 网页数据的起始时间的格式
        format_date_begain = date_begain.strftime('%m%d%Y')

        return format_date_begain

    # 获取下一页图片的url
    def get_next_page_url(self, url, date):

        year, month, days = int(date[4:]), int(date[:2]), int(date[2:4])
        date = datetime.date(year, month, days)
        next_date = date - datetime.timedelta(1)
        format_next_date = next_date.strftime('%m%d%Y')

        next_page_url = ''.join([url[:-8], format_next_date])
        return next_page_url


    # 保存每一个品牌的所有图片的url
    def save_each_img_url(self, this_url, this_search, img_quantity=0):

        self.down_record[this_search] = {}
        self.down_record_2[this_search] = {}
        next_page = True    # 用于控制爬取程序结束的
        now_page = 0        # 用于判断是否为第一页

        test_end = []

        while next_page:

            now_page +=1

            # 判断是不是第一页
            if now_page == 1:
                useful_url = this_url
            else:
                useful_url = self.get_next_page_url(this_url, date=last_one_date)

            each_url_pyquery = pq(useful_url, headers=get_headers(cookies=''))


            # 下载图片url

            # 每页最后一张图日期的前一天,作为下一页的开始
            last_one_name = self.get_img_name(info=each_url_pyquery, index=len(each_url_pyquery('img.img-postload'))-1)
            last_one_date = time.strftime('%m%d%Y', time.strptime(last_one_name, '%Y-%m-%d'))

            # 如果,发现最后一张图的日期与上一次的重复了
            if last_one_date in test_end:
                next_page = False
                self.down_quantity[this_search] = img_quantity

            test_end.append(last_one_date)


            for i in xrange(0, len(each_url_pyquery('img.img-postload'))):

                # 检测图片是否已经下载, 如已经下载了, 跳出while循环, 下一品牌
                img_name = self.get_img_name(info=each_url_pyquery, index=i)

                # 如果发现存储的图片url重复, 意味着这个品牌的所有图片url都已经存储完毕了
                if img_name in self.down_record[this_search].keys():
                    continue
                else:

                    imgurl_postfix = each_url_pyquery('img.img-postload')[i].attrib['src']  # 获取每张图片url的postfix
                    imgurl = ''.join([self.domain, imgurl_postfix])

                    imgurl_2_postfix = '/image/get/?brand={brand_name}&source=website&device=mobile' \
                                       '&mmddyyyy={date}&thumbSize=0&captureIndex=0'.format(brand_name=this_search, date=time.strftime('%m%d%Y', time.strptime(img_name, '%Y-%m-%d')))       # 大图
                    imgurl_2 = ''.join([self.domain, imgurl_2_postfix])

                    self.down_record[this_search][img_name] = imgurl
                    self.down_record_2[this_search][img_name] = imgurl_2


                    img_quantity += 1

            # sleep
            sleep_t = random.uniform(3.12, 5.55)
            time.sleep(sleep_t)

    # 遍历所有品牌
    def travel_each_brand(self):
        df_brand = pd.read_excel(self.excel_loc)

        for i in xrange(0, len(df_brand.index)):

            brand_name = df_brand.ix[i + 1, 'brand']    # 读取每个brand_name从excel中
            if brand_name in self.brand_done:
                continue

            else:
                brand_url = ''.join(
                    ['domain', 'other', self.get_now_date()])
                self.save_each_img_url(this_url=brand_url, this_search=brand_name)

                self.brand_done.append(brand_name)
                print ''.join([brand_name, ': ', time.strftime('%H:%M:%S', time.localtime())])   # 输出每个品牌下载完后的时间


        if i + 1 % 5 == 0:
            print 'Progress of rate is {count}'.format(count=self.i + 1)

        if i + 1 % 30 == 0:
            save_to_excel(self.down_record, self.down_record_2)


        # 算个时间
        print time.strftime('%H:%M:%S', time.localtime())




# 存到excel中
def save_to_excel(l1, l2):
    record_df = pd.DataFrame(l1)
    record_df_2 = pd.DataFrame(l2)

    record_df.to_excel('path')
    record_df_2.to_excel('path')

def get_headers(cookies=''):
    user_agent_list = ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
                       'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                       'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
                       'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',]
    user_agent = random.choice(user_agent_list)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Cookie': '{cookie}'.format(cookie=cookies),
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': '{user_agent}'.format(user_agent=user_agent)
    } if len(cookies) > 0 else {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': '{user_agent}'.format(user_agent=user_agent)
    }

    return headers



def main():
    test = down_img_url()
    test.travel_each_brand()

if __name__ == "__main__":
    main()
