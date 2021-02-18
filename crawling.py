import os
import sys
import json
from collections import OrderedDict
from time import sleep
from selenium import webdriver
from category_list import beauty_list, health_food_list, life_list

data = OrderedDict()

goods_list = {
  'beauty_list': beauty_list, 
  'health_food_list': health_food_list, 
  'life_list': life_list
}

url = 'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo='

driver = webdriver.Chrome("C:\\Python38\\chromedriver")

def get_product_info(index, big_list, mid_list, small_list, category):
  '''
  number : 단일 String
  img : 단일 String (src)
  brand : 단일 String
  name : 단일 String
  score : 단일 String
  review_count : 단일 String (**건)
  category_list : String 리스트 
  is_discount : boolean (할인 여부)
  discount_price : 단일 String (**원)
  origin_price : 단일 String (**원)

  옵션이 없는 단일 상품의 경우, 옵션 개수를 0개로 할 것인가 1개로 할 것인가
  그리고 옵션 이름 목록과 가격에 그냥 name과 price를 넣어야 하나?

  option_count : 단일 String (옵션 개수)
  option_name_list : String 리스트 (옵션별 이름)
  option_price_list : String 리스트 (옵션별 가격)
  option_img_list : String 리스트 (옵션별 이미지 src)
  '''

  sleep(1)

  number = driver.find_element_by_class_name('prd_btn_area > .btnZzim').get_attribute('data-ref-goodsno')
  img = (driver.find_element_by_id('mainImg')).get_attribute('src')
  brand = (driver.find_element_by_class_name('prd_brand')).text
  name = (driver.find_element_by_class_name('prd_name')).text
  review = (driver.find_element_by_id('repReview')).text.split('\n')[1]
  score = review.split()[0]
  review_count = review.split()[1].strip('()')

  option_name = []
  option_name_list = []
  option_price_list = []
  option_img_list = [img]

  cat = driver.find_elements_by_class_name('loc_history > li > .cate_y')
  category_list = [c.text for c in cat]
  
  discount_price = (driver.find_element_by_class_name('price-2')).text.split('\n')[0]

  try:
    origin_price = (driver.find_element_by_class_name('price-1')).text.split('\n')[0]
    is_discount = True
  except:
    origin_price = discount_price
    is_discount = False

  try:
    # 팔레트에서 상품에 '오늘드림'이 안 붙은 거에서부턴 밀림^^이런
    driver.find_element_by_class_name('prd_option_box').click()
    option_values = driver.find_elements_by_class_name('type1 > a > div > .option_value')
    if not option_values:
      option_values = driver.find_elements_by_tag_name('li > a > div > .option_value')

    for i in range(0, len(option_values)):
      option_name = option_values[i].text.split('\n')  # 옵션명, 가격만 나옴
    
    option_name = list(filter(lambda x : x != '오늘드림', option_name))
    option_name = [option_values[i].text.split('\n') for i in range(0, len(option_values))]
    option_name_list = [option[0] for option in option_name]

    option_count = 1 if option_values == 1 else len(option_values)

    for j in range(len(option_name_list)):
      if option_name_list[j].find('(품절)') != -1:
        option_price_list.append(discount_price)
      else:
        option_price_list.append(option_name[j][1].rstrip('원'))

    # 이미지가 없는 경우 그냥 pass시켜버려서 밑에다가 넣음
    option_imgs = driver.find_elements_by_class_name('type1 > a > span > img')
    option_img_list = [img.get_attribute('src') for img in option_imgs]

  except:
    # 품절일 때 option_count = 0이 돼서 가격이 안 나옴
    option_count = 0

  data["category_list"] = category_list
  data["name"] = name
  data["number"] = number
  data["brand"] = brand
  data["img"] = img
  data["brand"] = brand
  data["score"] = score
  data["review_count"] = review_count
  data["is_discount"] = is_discount
  data["discount_price"] = discount_price
  data["origin_price"] = origin_price
  data["option_count"] = option_count
  data["option_name_list"] = option_name_list
  data["option_price_list"] = option_price_list
  data["option_img_list"] = option_img_list

  try:
    with open(
      './data/{0}/{1}/{2}/{3}/{4}.json'.format(big_list, mid_list, small_list, category, number), 
      'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent="\t")
  except:
    os.makedirs('./data/{0}/{1}/{2}/{3}'.format(big_list, mid_list, small_list, category))

  driver.back()
  sleep(0.5)

for big_list in goods_list:
  for mid_list in goods_list[big_list]:
    print(mid_list)
    for small_list in goods_list[big_list][mid_list]:
      print(small_list)
      for category in goods_list[big_list][mid_list][small_list]:
        print(category)
        driver.get(url+goods_list[big_list][mid_list][small_list][category])
        driver.implicitly_wait(1)
        count = 0
        
        item_list = driver.find_elements_by_xpath('//li[@criteo-goods]')
        print(len(item_list))

        for index in range(len(item_list)): 
          item = driver.find_element_by_xpath(
            '//*[@id="Contents"]/ul[%s]/li[%s]/div/a' 
            % ((count // 4) + 2, (count % 4) + 1)
          )
          item.click()
          get_product_info(index, big_list, mid_list, small_list, category)
          count += 1
  
driver.quit()