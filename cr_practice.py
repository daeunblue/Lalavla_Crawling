import os
import sys
import json
import pymysql.cursors
from collections import OrderedDict
from time import sleep
from selenium import webdriver
from lalavla_category import category_list
  
# 크롬드라이버 위치 절대경로로 설정
driver = webdriver.Chrome("/Users/gimda-eun/Downloads/chromedriver")
url = 'https://m.lalavla.com/service/products/productDetail.html?prdId=10006070' 
driver.get(url)

def is_optional_product(n):
  return n > 0

def is_discount_product(dis, org):
  return dis != org

def get_product_info(big_list, mid_list, small_list, category):

  sleep(1)
  
  number = driver.find_element_by_xpath('/html/head/meta[16]').get_attribute('content')
  # prdImgSwiper > div > img  // 상품 메인img가 그냥 img태그, id 도 따로 안주어져있음.. 
  img = (driver.find_element_by_css_selector('#prdImgSwiper > div > img')).get_attribute('src')
  brand = (driver.find_element_by_class_name('category')).text
  name = (driver.find_element_by_class_name('prd-name')).text
  # 26~28은 뒤에 [1][0]이 어떤의미인지..? 
  # lalavla는 rapReview같은 창은 없고.. 따로 리뷰칸을 열어야하는데 열어도 수치가 적힌게 아니라 별모양 5개를 두고, style ="width:80%;"이런식으로 별 4개를 채움
  # 이부분을 어떻게 해야할지..?
  review = (driver.find_element_by_id('repReview')).text.split('\n')[1]
  rate = review.split()[0]
  review_count = review.split()[1].strip('()')
  
  # lalavla는 화면에 category 요소가없음... 38~39은 적용불가..
  cat = driver.find_elements_by_class_name('loc_history > li > .cate_y')
  category_list = [c.text for c in cat]
  
  discount_price = (driver.find_element_by_class_name('price-last')).text.split('\n')[0]

  # 할인 여부 확인
  try:
    # 할인 상품인 경우 .price-dis 요소가 있음
    origin_price = (driver.find_element_by_class_name('price-dis')).text.split('\n')[0]
    is_discount = True
  except:
    # 할인이 아닌 경우 discount_price가 곧 origin_price / 즉, 어느 경우든 discount_price가 해당 상품의 최종가
    origin_price = discount_price
    is_discount = False

  origin_price = origin_price.replace(',', '')
  discount_price = discount_price.replace(',', '')
  
  option_name_list = []
  option_price_list = []
  option_img_list = [img]


  try:
    # 단일 옵션인 경우 opt-only-one 라는 클래스가 있음, optEditMode // 옵션이 많으면 optSelectMode   (except로 넘어감)
    # .top-option을 클릭해야 .optSelectMode 인지 바로 optEditMode인지 확인가능 --> 옵션 선택시 optEditMode로 넘어감
    driver.find_element_by_class_name('top-option').click()
    
    
    # < 옵션 , 가격 정리하는 코드 > 
  except:
    print("실패")
    driver.quit()



