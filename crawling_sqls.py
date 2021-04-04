import os
import sys
import json
import pymysql.cursors
from collections import OrderedDict
from time import sleep
from selenium import webdriver
from lalavla_category import category_list as cat_list
from lalavla_category_list import lv_category_list as lv_list
import re

# 크롬드라이버 위치 절대경로로 설정
driver = webdriver.Chrome("/Users/gimda-eun/Downloads/chromedriver")
url = 'https://m.lalavla.com/service/products/productCategory.html?CTG_ID='
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

def width_to_rate(width): # 별점 
  if width == '100':
    return 5.0
  elif width == '80':
    return 4.0
  elif width == '60':
    return 3.0
  elif width == '40':
    return 2.0
  elif width == '20':
    return 1.0
  else : 
    return 0.0

def is_product_sold_out (option_list) : # 옵션 품절인지 확인하고 product_soldout 에 Y,N 입력
  product_soldout = []
  for i in option_list:
    try :
      class_name = i.get_attribute('class')
      if class_name == 'dis-out' :
        product_soldout.append('Y')
      else :
        product_soldout.append('N')
    except :
      product_soldout.append('N')

  return product_soldout


def get_product_info(big_list, mid_list, small_list):
  '''
  category_list : String. 대 + 중 + 소 카테고리 
  name : String. 상품 이름
  number : String 상품 고유 번호
  brand : String 브랜드 이름
  item_img_list : list(String). 상품 대표 이미지들의 리스트 
  product_img_list : list(String). 상품 설명 본문 이미지들의 리스트 
  rate : String. 평점
  review_count : String (**건) 상품의 리뷰 개수
  is_discount : boolean. 할인 여부
  origin_price : String (**원). 정상가
  discount_price : String (**원). 할인 가격
  /option_lists : 옵션 품절 여부 (Y : 품절,  N : 품절 아님)
  /option_count : String. 옵션 개수
  /option_name_list : list(String). 옵션별 이름
  /option_price_list : list(String). 옵션별 가격
  '''
  category_list = big_list+ ' '+ mid_list + ' '+ small_list  

  sleep(1.0)
  print(category_list)

  sqls = []
  product_img_list = []
  option_name_list = []
  option_price_list = []
  sold_out = 0
  option_count = 0 
  store_count = 35

  ##  name, number, brand  가져오기
  name = (driver.find_element_by_class_name('prd-name')).text
  number = driver.find_element_by_xpath('/html/head/meta[16]').get_attribute('content')
  brand = (driver.find_element_by_class_name('category')).text
  img = (driver.find_element_by_css_selector('#prdImgSwiper > div > img')).get_attribute('src')

  ## product_img_list 
  item_imgs = driver.find_elements_by_css_selector('#prdImgSwiper > div > img')
  item_img_list = [img.get_attribute('src') for img in item_imgs]

  ## item_img_list 
  product_imgs = (driver.find_elements_by_css_selector('#prdDtlTabImg img'))
  product_img_list = [itm_img.get_attribute('src') for itm_img in product_imgs]

  # rate & review_count 
  # Review 부분은 다음에 구현 (어떻게 얻어오는지만 이해하기)
  width = (driver.find_element_by_class_name('tit-area .inner')).get_attribute('style')
  re_width = re.split(' |%',width)
  rate = width_to_rate(re_width[1])
  
  org_review_count = driver.find_element_by_class_name('tit-area .num').text
  review_re = org_review_count.replace('(',')')
  review_count = review_re.replace(')','')

  ## is_discount ~ discount_price 
  discount_price = ((driver.find_element_by_class_name('price-last')).text.split('원')[0]).replace(',','')
  origin_price = ((driver.find_element_by_class_name('price-dis')).text.split('원')[0]).replace(',','')
  
  
  # 할인 X -> origin_price = discount_price
  if origin_price == '': 
    origin_price  = discount_price
    is_discount = False
  # 할인 O 
  else :
    is_discount = True 


# option_count ~ 끝까지
  try:
    # .top-option을 클릭해야 .optSelectMode 인지 바로 optEditMode인지 확인가능 --> 옵션 선택시 optEditMode로 넘어감
    driver.find_element_by_class_name('top-option').click()
    try:
      # 옵션이 많으면 optSelectMode // 단일 옵션인 경우 opt-only-one 라는 클래스가 있음, optEditMode (except로 넘어감)
      driver.find_element_by_class_name('optSelectMode')

      options_name = driver.find_elements_by_class_name('prd-item > .txt')
      options_price = driver.find_elements_by_class_name('prd-item > .right > .font-num-bold')

      option_name_list = [name.get_attribute('textContent') for name in options_name]
      option_price_list = [price.get_attribute('textContent') for price in options_price]

      option_count = len(option_name_list)

      print(option_name_list)

      # 옵션 품절 여부 확인
      option_list = driver.find_elements_by_css_selector('.option-list li')
      option_lists = is_product_sold_out(option_list) 

    except:
      # 단일 옵션인 경우 , option_count = 1
      option_count = 1
      option_name = (driver.find_element_by_class_name('option-view > .name')).get_attribute('textContent')
      option_price = ((driver.find_element_by_class_name('option-view > .price-area > .font-num')).get_attribute('textContent')).replace(',','')

      option_name_list.append(option_name)
      option_price_list.append(option_price)  
  except:
    # 제품 자체 품절 -> top-option.click 불가능 --> 긁어오지 않기 ! (함수 중단)
    driver.back() # 뒤로가기
    sleep(1.0)
    return 0


  # # json data
  # data["category_list"] = category_list
  # data["name"] = name
  # data["number"] = number
  # data["brand"] = brand
  # data["img"] = img
  # data["item_img_list"] = item_img_list
  # data["rate"] = rate
  # data["review_count"] = review_count
  # data["is_discount"] = is_discount
  # data["origin_price"] = origin_price
  # data["discount_price"] = discount_price
  # data["option_count"] = option_count
  # data["option_name_list"] = option_name_list
  # data["option_price_list"] = option_price_list

  # try:
  #   with open(
  #     './data/{0}/{1}/{2}/{3}.json'.format(big_list, mid_list, small_list, number), 
  #     'w', encoding='utf-8') as f:
  #     json.dump(data, f, ensure_ascii=False, indent="\t")
  # except: # 디렉터리가 없을 때만 디렉터리를 만듦
  #   os.makedirs('./data/{0}/{1}/{2}'.format(big_list, mid_list, small_list))

  
 
  # caterogy_item 테이블 (category_id = category 테이블 FK )
  # 최하위 카테고리 가져오기 (small_list가 없는 경우 -> mid_list)
  big_mid_cat_name = big_list+ ' '+ mid_list 
  find_category_id = ''
 
  # select문 사용해서 brand.name을 찾아서 brand_id 값 받아와서 item_brand_id 에 넣는 로직
  # cursors.fetchone()은 결과 값을 tuple 형태로 반환 -> brand_id_tuple[0] 이 우리가 필요한 실제 값 --> int 타입이기 떄문에 형변환 필요 X
  try:
    cursors.execute("select brand_id from brand where brand_name = '" + brand + "';")
    brand_id_tuple = cursors.fetchone()
    brand_id = brand_id_tuple[0]

    # small_list 없을 때 (남성, 건강식품 - 비타민, 일반식품)
    if big_mid_cat_name in small_list:
      find_category_id = mid_list    
    else:
      find_category_id = small_list

    cursors.execute(" select category_id from category where name = '" + find_category_id + "';")
    category_id_tuple = cursors.fetchone()
    category_id = category_id[0]

  except: # DB에 없는 브랜드일 경우 --> 안가져옴
    driver.back() # 뒤로가기
    sleep(1.0)
    return 0
  
  

# 옵션 품절인지 확인 --> 재고 넣을때 품절인 옵션을 제외하고 나눠야하기 때문
sold_out_count = 0
for i in range(len(option_lists)):
  if option_lists[i] == 'Y':
    sold_out_count += 1

# stock(매장별 재고) : 3500(전체 수량) % 매장 수 % 옵션 개수 
# 옵션별 재고량 list : options_quantity_list[i] = item_option.stock_quantity
options_quantity_list = [] 
stock_st = 3500 / store_count  
stock = divmod(stock_st, (option_count - sold_out_count)) 

cnt = 0
for q in range(option_count):
  if stock[1] != 0.0 : # 나머지가 있는 경우
    if option_lists[0] == 'Y': # 1번 옵션이 품절인 경우
      if option_lists[q] == 'N': # 옵션 품절아닌 경우
        if cnt == 1:
          options_quantity_list.append(int(stock[0]+stock[1]))
        else:
          options_quantity_list.append(int(stock[0]))
        cnt += 1   
      else : # 옵션 품절 -> 재고 0
        options_quantity_list.append(0)
        cnt += 1  
    else :
      if option_lists[q] == 'N': 
        if cnt == 0:
          options_quantity_list.append(int(stock[0]+stock[1]))
        else:
          options_quantity_list.append(int(stock[0]))
      else : # 옵션 품절 -> 재고 0
        options_quantity_list.append(0)
  else: # 나머지가 없는 경우
    if option_lists[q] == 'N': # 옵션 품절아닌 경우
      options_quantity_list.append(int(stock[0]))
    else : # 옵션 품절 -> 재고 0
      options_quantity_list.append(0)


  ## sql문 생성
  sqls = []

  # item 테이블
  sqls.append("insert into item(barcode, discount_price, is_optional, is_testable, item_img, item_name, item_price, stock_quantity, brand_id) \
       value(%d, %d, '%s', '%s', '%s', '%s', %d, %d, %d);" %(1, int(discount_price), is_optional_product(option_count), 1, img, name, int(discount_price),int(stock_st) brand_id))

  # item_id 가져오기 (int)
  try:
    ## cursors.execute("select item_id from item where item_name =  '" + name + "';")
    cursors.execute("select item_id from item where item_name =  'name';")    
    item_id_tuple = cursors.fetchone()
    item_id = item_id_tuple[0]
  except: 
    driver.back() # 뒤로가기
    sleep(1.0)
    return 0

  # category_item 테이블
  sqls.append("insert into category_item(category_id, item_id)\
      value(%d, %d);" %(category_id, item_id))

  # item_img 테이블 (상품 대표 이미지)
  for l in range(len(item_img_list)):
    sqls.append("insert into item_img(item_img, item_id) \
      values('%s', %d);" %(item_img_list[l],item_id))

  # item_option 테이블
  m = 0
  if is_optional_product(option_count) == 'Y':
    # 단일 옵션인지 확인
    if option_count != 1:         
      for m in range(option_count):
        if option_lists[m] == 'Y':
          sqls.append("insert into item_option(item_option_name, stock_quantity, item_id) \
            values('%s', %d, %d);" %(option_name_list[m],options_quantity_list[m],item_id))
        else: # 옵션 품절 
          sqls.append("insert into item_option(item_option_name, stock_quantity, item_id) \
            values('%s', %d, %d);" %(option_name_list[m],0,item_id))
    else: # 단일 옵션인 경우
       sqls.append("insert into item_option(item_option_name, stock_quantity, item_id) \
            values('%s', %d, %d);" %(option_name_list[m],options_quantity_list[m],item_id))

  
  # product_img 테이블
  for b in range(len(product_img_list)):
  sqls.append("insert into product_img(product_img, item_id) \
    values('%s', %d);" %(product_img_list[b],item_id))

  # item_option_id 가져오기
  try:
    cursors.execute("select item_option_id from item where item_id =  '" + item_id + "';")
    item_option_id_tuple = cursors.fetchall()
    item_option_id_list = [x[0] for x in item_option_id_tuple] # 각 튜플의 첫번째 element만 list 형태로 추출 [1, 22, 53, 44, 1]
  except: 
    driver.back() # 뒤로가기
    sleep(1.0)
    return 0

  # store_quantity 테이블
  for k in range(len(item_option_id_list)):
    for i in range(1,36): # store : 35 곳
      sqls.append("insert into store_quantity(stock_quantity, item_id, item_option_id, store_id) \
        values(%d, %d, %d, %d);" %(options_quantity_list[k],item_id, item_option_id_list[k],i))


  driver.back() # 뒤로가기
  sleep(1.0)




def load_cat_list():
  for big_list in cat_list: # big_list는 cat_list에 String
    for mid_list in cat_list[big_list]: # mid_list는 String
      driver.get(url+"C040300")
      driver.implicitly_wait(3)
      # 스크롤을 하지 않으면 not clickable 오류가 뜸
      # 따라서, 매 루프마다 모니터 세로 화면의 절반만큼 스크롤을 내릴 수 있도록
      # scroll_Height를 미리 구해 둠
      scroll_height = 360.2

      cats = driver.find_elements_by_class_name('swiper-slide > a')
      # 카테고리 한글 이름이 필요할 경우 cats_name 쓸 것
      cats_name = [cat.text for cat in cats]

      # cat_index로 tiny_list의 몇 번째 카테고리를 클릭할지 정함
      # ex) 전체 / 기초세트 / 스킨,토너 / 로션 / 에센스,세럼,앰플 / ...        
      if cats:
        for cat_index in range(1,2):
          items = driver.find_elements_by_class_name('prd-list > ul > li > a')          
          height = driver.execute_script('return (window.innerHeight || document.body.clientHeight)')

          for index in range(len(items)): 
            if cat_index:
              try:
                cats = driver.find_elements_by_class_name('swiper-slide > a')
                cats[cat_index].click()
                sleep(0.7)
              except:
                driver.back() # 뒤로가기
                sleep(4.0)
                
            
            try:
              items = driver.find_elements_by_class_name('prd-list > ul > li > a')
              height += scroll_height 
              driver.execute_script('window.scrollTo(0, ' + str(height) + ')')
              sleep(1.0)

              items[index].click()
              driver.implicitly_wait(3)

              get_product_info(big_list, mid_list, cats_name[cat_index])
            except:
              driver.back() # 뒤로가기
              sleep(4.0)

      
      else:
        items = driver.find_elements_by_class_name('prd-list > ul > li > a')
        height = driver.execute_script('return (window.innerHeight || document.body.clientHeight)')

        for index in range(len(items)):
          try:
            items = driver.find_elements_by_class_name('prd-list > ul > li > a')
            height += scroll_height 
            driver.execute_script('window.scrollTo(0, ' + str(height) + ')')
            sleep(0.5)

            items[index].click()
            driver.implicitly_wait(3)

            get_product_info(big_list, mid_list, '전체')
          except:
            driver.back() # 뒤로가기
            sleep(4.0)
            pass



if __name__ == '__main__':
  print('crawling.py main 실행')

  conn = pymysql.connect(
    host = '3.34.117.216', # 로컬호스트
    user = 'dayang',  # 유저
    password = 'dayang',  # 비밀번호
    db = 'test',  # 데이터베이스
    charset = 'utf8'  # 인코딩 캐릭터셋
  )

  cursors = conn.cursor()
  print('DB 연동 완료')

  load_cat_list()  
  driver.quit()

else:
  print('crawling.py is imported')