'''
올리브영 세부 카테고리에서 1페이지에 있는 상품들의 정보를 가져와
상품 1개씩 순차적으로 data 디렉터리 밑 세부 카테고리 디렉터리에
상품번호.json으로 저장하는 코드
작성자 : github @dev-dain
'''
import os
import sys
import json
import pymysql.cursors
from collections import OrderedDict
from time import sleep
from selenium import webdriver
from category_list import beauty_list, health_food_list, life_list

goods_list = {
  'beauty_list': beauty_list, 
  'health_food_list': health_food_list, 
  'life_list': life_list
}
truth_table = {'True': 'Y', 'False': 'N'}

# 크롬드라이버 위치 절대경로로 설정
driver = webdriver.Chrome("C:\\Python38\\chromedriver")
url = 'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo='
data = OrderedDict()


def is_optional_product(n):
  return n > 0

def is_discount_product(dis, org):
  return dis != org

def execute_sql(sqls):
  for sql in sqls:
    print(sql)
    cursors.execute(sql)
    conn.commit()

# 대/중/소/카테고리를 넘김
# ex) 뷰티(big) > 스킨케어(mid) > 페이셜케어(small) > 스킨/토너(category)
def get_product_info(big_list, mid_list, small_list, category):
  '''
  category_list : list(String). 해당 상품의 중/소/카테고리 
  name : String. 상품 이름
  number : String. 상품 고유번호
  brand : String. 브랜드 이름
  img : String (src). 대표 이미지 -> 복수 개일 수 있으므로 변경 필요 
  product_img_list : list(String). 대표 이미지들의 리스트
  item_img_list : list(String). 상품 설명 본문 이미지들의 리스트
  rate : String. 평점
  review_count : String (**건) 상품의 리뷰 개수
  is_discount : boolean. 할인 여부
  origin_price : String (**원). 정상가
  discount_price : String (**원). 할인 가격

  옵션이 없는 단일 상품의 경우, 옵션 개수를 0개로 할 것인가 1개로 할 것인가
  그리고 옵션 이름 목록과 가격에 그냥 name과 price를 넣어야 하나?
  품절의 경우 옵션 가격은 얼마?

  option_count : String. 옵션 개수
  option_name_list : list(String). 옵션별 이름
  option_price_list : list(String). 옵션별 가격
  option_img_list : list(String). 옵션별 이미지 src
  '''

  sleep(1)

  number = driver.find_element_by_class_name('prd_btn_area > .btnZzim')\
    .get_attribute('data-ref-goodsno')
  img = (driver.find_element_by_id('mainImg')).get_attribute('src')
  brand = (driver.find_element_by_class_name('prd_brand')).text
  name = (driver.find_element_by_class_name('prd_name')).text
  review = (driver.find_element_by_id('repReview')).text.split('\n')[1]
  rate = review.split()[0]
  review_count = review.split()[1].strip('()')

  cat = driver.find_elements_by_class_name('loc_history > li > .cate_y')
  category_list = [c.text for c in cat]
  
  discount_price = (driver.find_element_by_class_name('price-2')).text.split('\n')[0]

  try:
    # 할인 상품인 경우 .price-1 요소가 있음
    origin_price = (driver.find_element_by_class_name('price-1')).text.split('\n')[0]
    is_discount = True
  except:
    # 할인이 아닌 경우 discount_price가 곧 origin_price
    # 즉, 어느 경우든 discount_price가 해당 상품의 최종가
    origin_price = discount_price
    is_discount = False

  origin_price = origin_price.replace(',', '')
  discount_price = discount_price.replace(',', '')
  
  option_name_list = []
  option_price_list = []
  option_img_list = [img]

  try:
    # 옵션이 없는 경우 .prd_option_box 요소가 없음 (except로 넘어감)
    # .prd_option_box를 클릭해야 .option_value가 드러남
    driver.find_element_by_class_name('prd_option_box').click()

    # 품절 상품인 경우 .type1 soldout임
    options = driver.find_elements_by_class_name('type1 > a > div > .option_value')

    if not options: # 옵션에 상품 이미지가 없는 경우 .type1 없이 <li class> 태그임
      # options 자체는 WebElement가 요소인 리스트임. option들을 가진 리스트
      options = driver.find_elements_by_tag_name('li > a > div > .option_value')

    # 옵션명, 가격이 차례로 요소로 들어간 리스트가 option_values가 됨
    # ex) ['04 데일리톡(리뉴얼)', '7,840원']
    # 이 때, 품절 상품의 경우 상품 이름만 요소로 들어감. 옵션 자체에 가격이 없음    
    option_values = [option.text.split('\n') for option in options]

    # 상품의 옵션 이름만 리스트로 뽑아옴
    option_name_list = [option[0] for option in option_values]
    option_count = len(options)

    for k in range(len(option_name_list)):
      # 품절일 경우, 기본가인 discount_price를 품절 상품 가격으로 둠
      if option_name_list[k].find('(품절)') != -1:
        option_price_list.append(discount_price)  
      else:
        option_price_list.append(option_values[k][1].rstrip('원'))

    # 옵션은 있으나 옵션에 이미지가 없는 경우 except로 넘어감
    # 옵션에 이미지가 있는 경우에만 option_img_list에 각 이미지를 넣음
    option_imgs = driver.find_elements_by_class_name('type1 > a > span > img')
    option_img_list = [img.get_attribute('src') for img in option_imgs]

  except:
    # 품절일 때 option_count = 0이 돼서 가격이 안 나옴
    option_count = 0

  try:
    # 대표 이미지가 여러 개일 경우
    product_imgs = driver.find_elements_by_class_name('prd_thumb_list > li > a')
    product_img_list = [img.get_attribute('data-img') for img in product_imgs]  
  except:
    product_img_list = [img]

  # 상품 본문 이미지를 차례로 크롤링
  item_imgs = driver.find_elements_by_class_name('detail_area img')
  item_img_list = [img.get_attribute('src') for img in item_imgs]

  data["category_list"] = category_list
  data["name"] = name
  data["number"] = number
  data["brand"] = brand
  data["img"] = img
  data["product_img_list"] = product_img_list
  data["item_img_list"] = item_img_list
  data["rate"] = rate
  data["review_count"] = review_count
  data["is_discount"] = is_discount
  data["origin_price"] = origin_price
  data["discount_price"] = discount_price
  data["option_count"] = option_count
  data["option_name_list"] = option_name_list
  data["option_price_list"] = option_price_list
  data["option_img_list"] = option_img_list

  try:
    with open(
      './data/{0}/{1}/{2}/{3}/{4}.json'.format(big_list, mid_list, small_list, category, number), 
      'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent="\t")
  except: # 디렉터리가 없을 때만 디렉터리를 만듦
    os.makedirs('./data/{0}/{1}/{2}/{3}'.format(big_list, mid_list, small_list, category))

  sqls = []
  sqls.append("insert into discount(is_discount, discount_price) \
    values (%s, %d);" % (is_discount_product(int(discount_price), int(origin_price)), int(discount_price)))
  sqls.append("insert into item(item_name, item_brand_id, item_img, item_price, category_name, is_optional, barcode, buy) \
    values ('%s', 1, '%s', %d, '%s', %s, %d, %d);" \
    % (name, img, int(discount_price), category_list[-1], is_optional_product(option_count), 1, 1))
  for i in range(len(item_img_list)):
    sqls.append("insert into item_img(item_id, item_img, item_order) \
      values(%d, '%s', %d);" % (1, item_img_list[i], i + 1))
  for l in range(len(product_img_list)):
    sqls.append("insert into product_img(item_id, product_img) values(%d, '%s');" % 
      (1, product_img_list[l]))

  # 품절인지 알아내는 로직이 필요
  if is_optional_product(option_count):
    for m in range(option_count):
      if option_count != len(option_img_list):
        sqls.append("insert into item_option(item_id, item_option_img, item_option_name, is_soldout) \
          values(%d, '%s', '%s', %s);" % (1, '', option_name_list[i], 'N'))
      else:
        sqls.append("insert into item_option(item_id, item_option_img, item_option_name, is_soldout) \
          values(%d, '%s', '%s', %s);" % (1, option_img_list[i], option_name_list[i], 'N'))
  
  execute_sql(sqls)

  driver.back() # 뒤로가기
  sleep(0.5)

def load_goods_list():
  for big_list in goods_list: # big_list는 goods_list에 String
    for mid_list in goods_list[big_list]: # mid_list는 String
      for small_list in goods_list[big_list][mid_list]: # small_list는 String
        for category in goods_list[big_list][mid_list][small_list]: # category는 String      
          driver.get(url+goods_list[big_list][mid_list][small_list][category])
          driver.implicitly_wait(1)
          count = 0 # count로 몇 번째 item의 정보를 가져올지 정함
        
          # 상품을 감싼 태그를 빼냄. 24/36/48개
          items = driver.find_elements_by_xpath('//li[@criteo-goods]')

          for index in range(len(items)): 
            # 개별 아이템을 고름
            item = driver.find_element_by_xpath(
              '//*[@id="Contents"]/ul[%s]/li[%s]/div/a' 
              % ((count // 4) + 2, (count % 4) + 1)
            )
            item.click()
            get_product_info(big_list, mid_list, small_list, category)
            count += 1


if __name__ == '__main__':
  print('crawling.py main 실행')

  # 이 부분은 DB 정보로 채울 것
  conn = pymysql.connect(
    host = '', # 로컬호스트
    user = '',  # 유저
    password = '',  # 비밀번호
    db = '',  # 데이터베이스
    charset = ''  # 인코딩 캐릭터셋
  )
  cursors = conn.cursor()
  print('DB 연동 완료')

  load_goods_list()  
  driver.quit()

else:
  print('crawling.py is imported')