import os
import sys
import json
import pymysql.cursors
from collections import OrderedDict
from time import sleep
from selenium import webdriver

driver = webdriver.Chrome("/Users/gimda-eun/Downloads/chromedriver")
url = 'https://m.lalavla.com/service/products/productDetail.html?prdId=10003882' 
driver.get(url)

try :

  driver.find_element_by_class_name('top-option').click()
  # selector : #prd-option > div.hidden-area > div.opt-wrap > div.scroll-cont > div.opt-select-wrap > ul > li:nth-child(2) > a > span.txt
  # xpath : //*[@id="prd-option"]/div[1]/div[2]/div[1]/div[1]/ul/li[1]/a/span[1]
  
  # opt_num : 옵션 총 개수
  opt_num = driver.find_elements_by_class_name('prd-item')

  i = 1

  for i in range(len(opt_num)):
    opt_names = driver.find_elements_by_css_selector('#prd-option > div.hidden-area > div.opt-wrap > div.scroll-cont > div.opt-select-wrap > ul > li:nth-child('+str(i)+') > a > span.txt')
   # opt_names = driver.find_element_by_xpath('//*[@id="prd-option"]/div[1]/div[2]/div[1]/div[1]/ul/li['+str(i)+']/a/span[1]')
    i += 1
    # 왜 text로 불러오려고하면 오류가 날까...
    print(opt_names.text)

except:
  driver.quit()
