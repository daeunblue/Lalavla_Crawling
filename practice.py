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


# img 있는지 check
def check_exist(path):
  try:
    driver.find_element_by_id("topvisual-image")
    return True
  except:
    return False
  
# brand name 
brand_lists = driver.find_elements_by_class_name('list-brdSrchResult > li > a')
brand_list = [brand.text for brand in brand_lists]


# 전체보기 클릭
driver.find_element_by_xpath("/html/body/section/div/a").click()
driver.implicitly_wait(1)


brand_img_lists = [] 

for k in range (2,17):
  for i in range (1,88):
    try:
      xpath_ = "/html/body/section/ul["+str(k)+"]/li["+str(i)+"]/a"
      menu = driver.find_element_by_xpath(xpath_).click()
      #요소가 로딩될때까지 암시적 대기
      driver.implicitly_wait(3)
      # img src exist check
      if check_exist(xpath_) == True :
        brand_img_lists.append(driver.find_element_by_id("topvisual-image").get_attribute("src"))
      else :
        brand_img_lists.append("NULL")
      driver.back()
    
    except:
      break


for i, name in enumerate(brand_list):
  data[name] = i , brand_img_lists[i]


driver.quit()

try:
  with open(
    './data/brand.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent="\t")
except: # 디렉터리가 없을 때만 디렉터리를 만듦
  os.makedirs('./data')

print("done!")