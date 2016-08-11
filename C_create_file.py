#-- coding=utf-8 --#
'''  Tristan SHi '''

import pandas as pd
# 创建新文件夹
class file:
    def __init__(self,
                 path='/Users/macbookpro/Desktop/python/crawler/task2/all_brand/',
                 excel='/Users/macbookpro/Desktop/python/crawler/task2/exist_brand.xlsx'):
        self.path = path
        self.excel = excel

    def create_new_file(self, brand_name):
        import os

        path = os.path.join(self.path, brand_name)
        if not os.path.isdir(path):
            os.makedirs(path)

        new_path = os.path.join(''.join([self.path, brand_name, '/']), 'small_img')
        if not os.path.isdir(new_path):
            os.makedirs(new_path)

        new_path_big = os.path.join(''.join([self.path, brand_name, '/']), 'long_img')
        if not os.path.isdir(new_path_big):
            os.makedirs(new_path_big)

        return

    def load_excel(self):
        df_brand = pd.read_excel(self.excel)
        for brand_name in df_brand['brand']:
            self.create_new_file(brand_name)

test = file()
test.load_excel()


