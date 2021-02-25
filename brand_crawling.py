'''
랄라블라 브랜드를 긁어와서 brand.json으로 저장하는 코드
현재 카테고리 밑에 data를 반드시 만들고 구동하세요
작성자 : github @dev-dain
'''

import os
import sys
import json
import pymysql.cursors
from collections import OrderedDict
from time import sleep
from selenium import webdriver

driver = webdriver.Chrome("/Users/gimda-eun/Downloads/chromedriver")
url = 'https://m.lalavla.com/service/main/mainBrand.html'
data = OrderedDict()

driver.get(url)
driver.implicitly_wait(1)

brand_lists = driver.find_elements_by_class_name('list-brdSrchResult > li > a')
brand_list = [brand.text for brand in brand_lists]
for i, name in enumerate(brand_list):
  data[name] = i
  
driver.quit()

try:
  with open(
    './data/brand.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent="\t")
except: # 디렉터리가 없을 때만 디렉터리를 만듦
  os.makedirs('./data')

print('done!')