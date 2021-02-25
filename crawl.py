from selenium import webdriver
from time import sleep
import os
import sys

def get_product_info(i):
  i_list = driver.find_elements_by_class_name('cate_prd_list > .flag')

  i_list[i].click()

  img = driver.find_element_by_id('mainImg')
  brand = driver.find_element_by_class_name('prd_brand')
  name = driver.find_element_by_class_name('prd_name')
  
  category = driver.find_elements_by_class_name('loc_history > li > .cate_y')
  for cat in category:
    print(cat.text, end=' ')
  
  print()
  discount_price = driver.find_element_by_class_name('price-2')
  
  try:
    origin_price = driver.find_element_by_class_name('price-1')
  except:
    origin_price = discount_price
  try:
    driver.find_element_by_class_name('prd_option_box').click()
    option_imgs = driver.find_elements_by_class_name('type1 > a > span > img')
    for img in option_imgs:
      pass
      #print(img.get_attribute('src'))
    
    option_values = driver.find_elements_by_class_name('type1 > a > div > span')
    for value in option_values:
      pass
    #print(value.text)
  except:
    pass
      #print('nothing')

    # print(img.get_attribute('src'))
  driver.back()
  sleep(2)

driver = webdriver.Chrome("C:\\Python38\\chromedriver")

code_list = [
  '10000010002', '10000010003', '10000010004',
  '10000010005', '10000010006', '10000010007', '10000010008',
  '10000020001', '10000020002', '10000020003',
  '10000030002', '10000030003', '10000030004'
]
url = 'https://www.oliveyoung.co.kr/store/main/main.do?oy=0'

driver.get(url)

for code in code_list:
  driver.execute_script('common.link.moveCategoryShop(%s)' % code)

  item_list = driver.find_elements_by_class_name('ct-product > .item')
  print(len(item_list))

  if not item_list:
    item_list = driver.find_elements_by_class_name('cate_prd_list')

    for i in range(len(item_list)):
      i_list = driver.find_elements_by_class_name('cate_prd_list > .flag')
      print(len(i_list))

      for i in range(len(i_list)):
        get_product_info(i)
        sleep(2)

    driver.back()
    sleep(2)

  for i in range(len(item_list)):
    i_list = driver.find_elements_by_class_name('ct-product > .item')
    print(len(i_list))

#   driver.get('https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000123879&dispCatNo=1000001000200060004&trackingCd=Drawer_Cat100000100020006_Cat')

    img = driver.find_element_by_id('mainImg')
    brand = driver.find_element_by_class_name('prd_brand')
    name = driver.find_element_by_class_name('prd_name')
    
    category = driver.find_elements_by_class_name('loc_history > li > .cate_y')
    for cat in category:
      print(cat.text, end=' ')
    print()
    
    discount_price = driver.find_element_by_class_name('price-2')
    
    try:
      origin_price = driver.find_element_by_class_name('price-1')
    except:
      origin_price = discount_price

    try:
      driver.find_element_by_class_name('prd_option_box').click()
      option_imgs = driver.find_elements_by_class_name('type1 > a > span > img')
      for img in option_imgs:
        pass
        #print(img.get_attribute('src'))
      
      option_values = driver.find_elements_by_class_name('type1 > a > div > span')
      for value in option_values:
        pass
        #print(value.text)
    except:
      pass
      #print('nothing')

    # print(img.get_attribute('src'))
    driver.back()
  
  driver.back()
  sleep(2)

driver.quit()