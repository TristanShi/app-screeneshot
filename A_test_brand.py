# -*- coding: utf-8 -*-
'''  Tristan Shi '''

'''
Test brand exist or not
'''
import requests
import pandas
import random
import time


class brand:

    def __init__(self, no_record=[], record=[], record_temp=[], txt='/Users/macbookpro/Desktop/URLs.txt', count=0):
        self.no_record = no_record
        self.record = record
        self.record_temp = record_temp
        self.count = count
        self.txt = txt

    def test(self):

        with open(self.txt, 'r') as f:
            for line in f:

                # 每个品牌的搜索过程的url
                each_brand = line.replace("\n", '')
                lower_each_brand = each_brand.lower()

                # 查是否已经测试过
                if each_brand in self.record_temp or each_brand in self.no_record or lower_each_brand in self.record:
                    continue

                else:
                    search_domain = ''.join(['domain', 'Brand/Search?searchString='])
                    each_brand_url = ''.join([search_domain, each_brand]) 

                    # 判断是否存在这个品牌, 不存在的话添加到测试列表
                    req = requests.get(each_brand_url)
                    if req.url.find('brand') == -1:
                        self.no_record.append(each_brand)
                    else:
                        self.record_temp.append(each_brand)
                        each_brand = req.url[req.url.find('list') + 5: -1]
                        self.record.append(each_brand)

                    self.count += 1
                    if self.count % 10 == 0:
                        print 'The number of brand is already tested: {count}, {brand}'.format(count=self.count,
                                                                                               brand=each_brand)  # 用format替代格式化字符%

                    req.close()
                    time.sleep(random.uniform(2.3, 6.71))

    def write_to_excel(self):
        non_exist_brand = pandas.DataFrame(self.no_record, columns=['brand'])
        exist_brand = pandas.DataFrame(self.record, columns=['brand'])

        non_exist_brand.index += 1
        exist_brand.index += 1

        non_exist_brand.to_excel('path')
        exist_brand.to_excel('path')

def main():
    test_brand = brand()
    test_brand.test()
    test_brand.write_to_excel()

if __name__ == "__main__":
    main()



