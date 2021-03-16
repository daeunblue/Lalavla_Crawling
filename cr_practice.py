import os
import sys
import json
import pymysql.cursors
from collections import OrderedDict
from time import sleep
from selenium import webdriver
from lalavla_category import category_list as cat_list
from list_practice import lv_category_list as lv_list
import re

# 크롬드라이버 위치 절대경로로 설정
driver = webdriver.Chrome("/Users/gimda-eun/Downloads/chromedriver")
url = 'https://m.lalavla.com/service/products/productCategory.html?CTG_ID='
data = OrderedDict()

# truth_table = {'True': 'T', 'False': 'F'}

def is_optional_product(n):
  if n > 0 :
    return 'Y'
  else :
    return 'N'


def is_discount_product(dis, org):
  return dis != org

def execute_sql(sqls):
  for sql in sqls:
    print(sql)
    cursors.execute(sql)
    conn.commit()

def width_to_rate(width): 
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

def is_product_sold_out (option_list) :
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


# 대/중/소/카테고리를 넘김
# ex) 스킨케어(big) > 기초스킨케어(mid) > 스킨/토너(small)
def get_product_info(big_list, mid_list, small_list):
  '''
  category_list : list(String). 해당 상품의 중/소/카테고리 --> 어디서 필요한지..?
  /name : String. 상품 이름
  /number : String. 상품 고유번호
  /brand : String. 브랜드 이름
  /img : String (src). 대표 이미지 -> 복수 개일 수 있으므로 변경 필요 
  /product_img_list : list(String). 대표 이미지들의 리스트
  /item_img_list : list(String). 상품 설명 본문 이미지들의 리스트
  /rate : String. 평점
  /review_count : String (**건) 상품의 리뷰 개수
  /is_discount : boolean. 할인 여부
  /origin_price : String (**원). 정상가
  /discount_price : String (**원). 할인 가격
  옵션이 없는 단일 상품의 경우, 옵션 개수를 0개로 할 것인가 1개로 할 것인가
  그리고 옵션 이름 목록과 가격에 그냥 name과 price를 넣어야 하나?
  품절의 경우 옵션 가격은 얼마?
  /option_lists : 옵션 품절 여부 (Y : 품절,  N : 품절 아님)
  /option_count : String. 옵션 개수
  /option_name_list : list(String). 옵션별 이름
  /option_price_list : list(String). 옵션별 가격

  '''
  category_list = big_list+ ' '+ mid_list + ' '+ small_list

  sleep(1.0)
  print(category_list)

  product_img_list = []
  option_name_list = []
  option_price_list = []
  sold_out = 0
  option_count = 0 
 
  ##  name, number, brand  가져오기
  name = (driver.find_element_by_class_name('prd-name')).text
  number = driver.find_element_by_xpath('/html/head/meta[16]').get_attribute('content')
  brand = (driver.find_element_by_class_name('category')).text
  img = (driver.find_element_by_css_selector('#prdImgSwiper > div > img')).get_attribute('src')


  
  ## product_img_list 
  product_imgs = driver.find_elements_by_css_selector('#prdImgSwiper > div > img')
  product_img_list = [img.get_attribute('src') for img in product_imgs]

  ## item_img_list 
  item_imgs = (driver.find_elements_by_css_selector('#prdDtlTabImg img'))
  item_img_list = [itm_img.get_attribute('src') for itm_img in item_imgs]

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
  
  
  # 할인 X -> price-dis 값 : ''
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
      option_name = (driver.find_element_by_class_name('option-view > .name')).get_attribute('textContent')
      option_price = ((driver.find_element_by_class_name('option-view > .price-area > .font-num')).get_attribute('textContent')).replace(',','')

      option_name_list.append(option_name)
      option_price_list.append(option_price)
    
      option_count = 1
  except:
    # 제품 자체 품절 -> top-option.click 불가능 --> option관련 정보 제외하고는 다 가져가야함
    sold_out = 1 
    
  

  # json data
  data["category_list"] = category_list
  data["name"] = name
  data["number"] = number
  data["brand"] = brand
  data["img"] = img
  data["item_img_list"] = item_img_list
  data["rate"] = rate
  data["review_count"] = review_count
  data["is_discount"] = is_discount
  data["origin_price"] = origin_price
  data["discount_price"] = discount_price
  data["option_count"] = option_count
  data["option_name_list"] = option_name_list
  data["option_price_list"] = option_price_list

  try:
    with open(
      './data/{0}/{1}/{2}/{3}.json'.format(big_list, mid_list, small_list, number), 
      'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent="\t")
  except: # 디렉터리가 없을 때만 디렉터리를 만듦
    os.makedirs('./data/{0}/{1}/{2}'.format(big_list, mid_list, small_list))

  search_category = big_list + ' ' + mid_list + ' ' + small_list
  sql_cat_name = ''
  for category_id, cat_name in lv_list.items(): #lv_list 아이템을 하나씩 접근해서, key, value를 각각 category_id, cat_name에 저장
    if category_id == search_category:
      sql_cat_name = cat_name
      # print (cat_name)
    
  # sql문 생성 + insert
  sqls = []
  sqls.append("insert into Discount(is_discount, discount_price) \
  values ('%s', %d);" % (is_discount_product(int(discount_price), int(origin_price)), int(discount_price)))


  # select문 사용해서 brand.name을 찾아서 brand_id 값 받아와서 item_brand_id 에 넣는 로직
  # cursors.fetchone()은 결과 값을 tuple 형태로 반환 -> brand_id_tuple[0] 이 우리가 필요한 실제 값 --> int 타입이기 떄문에 형변환 필요 X
  cursors.execute("select brand_id from Brand where brand_name = '"+brand+"';")
  brand_id_tuple = cursors.fetchone()
  brand_id = brand_id_tuple[0]

  # item.category_name
  for i in range(len(item_img_list)):
    sqls.append("insert into Item_img(item_img, item_order) \
      values('%s', %d);" % ( item_img_list[i], i + 1))

  # 제품 자체가 품절인지 확인하는 로직 필요
  if sold_out == 0 :
    sqls.append("insert into Item(item_name, item_brand_id, item_img, item_price, category_name, is_optional, barcode, buy, item_no, is_soldout) \
      values ('%s', %d, '%s', %d, '%s', '%s', %d, %d, '%s','%s');" % (name, brand_id, img, int(discount_price), sql_cat_name, is_optional_product(option_count), 1, 1, number, 'N'))
  else:
    sqls.append("insert into Item(item_name, item_brand_id, item_img, item_price, category_name, is_optional, barcode, buy, item_no, is_soldout) \
      values ('%s', %d, '%s', %d, '%s', '%s', %d, %d, '%s','%s');" % (name, brand_id, img, int(discount_price), sql_cat_name, is_optional_product(option_count), 1, 1, number, 'N'))
  

  # 품절인지 알아내는 로직이 필요
  m = 0
  if is_optional_product(option_count) == 'Y':
    # 단일 옵션인지 확인
    if option_count != 1:         
      for m in range(option_count):
        if option_lists[m] == 'Y':
          sqls.append("insert into Item_option(item_no, item_option_name, is_soldout) \
            values('%s', '%s', '%s');" %(number, option_name_list[m],'Y'))
        else:
          sqls.append("insert into Item_option(item_no, item_option_name, is_soldout) \
            values('%s', '%s', '%s');" %(number, option_name_list[m],'N'))
    else: # 단일 옵션인 경우
      sqls.append("insert into Item_option(item_no, item_option_name, is_soldout) \
        values('%s', '%s', '%s');" %(number, option_name_list[m],'N'))


  for i in range(len(item_img_list)):
    sqls.append("insert into Item_img(item_no, item_img, item_order) \
      values('%s', '%s', %d);" % (number, item_img_list[i], i + 1))
      
  # 본문 이미지
  for l in range(len(product_img_list)):
    sqls.append("insert into Product_img(item_no, product_img) \
      values('%s', '%s');" % (number, product_img_list[l]))

  # 카테고리 대, 중, 소 넘기기
  # sqls.append("insert into Category_detail(category_one, category_two, category_three) \
  #   valus('%s', '%s', '%s');" %(big_list, mid_list, small_list))

  f = open("sql.txt",'a')
  for i in sqls:
    f.write(i)
    f.write('\n')

  execute_sql(sqls)

  driver.back() # 뒤로가기
  sleep(1.0)

  
def load_cat_list():
  for big_list in cat_list: # big_list는 cat_list에 String
    for mid_list in cat_list[big_list]: # mid_list는 String
      driver.get(url+cat_list[big_list][mid_list]['all'])
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
        for cat_index in range(len(cats)):
          items = driver.find_elements_by_class_name('prd-list > ul > li > a')          
          height = driver.execute_script('return (window.innerHeight || document.body.clientHeight)')

          for index in range(len(items)): 
            if cat_index:
              cats = driver.find_elements_by_class_name('swiper-slide > a')
              cats[cat_index].click()
              sleep(0.3)

            items = driver.find_elements_by_class_name('prd-list > ul > li > a')
            height += scroll_height 
            driver.execute_script('window.scrollTo(0, ' + str(height) + ')')
            sleep(0.5)

            items[index].click()
            driver.implicitly_wait(3)

            get_product_info(big_list, mid_list, cats_name[cat_index])
      
      else:
        items = driver.find_elements_by_class_name('prd-list > ul > li > a')
        height = driver.execute_script('return (window.innerHeight || document.body.clientHeight)')

        for index in range(len(items)):
          items = driver.find_elements_by_class_name('prd-list > ul > li > a')
          height += scroll_height 
          driver.execute_script('window.scrollTo(0, ' + str(height) + ')')
          sleep(0.5)

          items[index].click()
          driver.implicitly_wait(3)

          get_product_info(big_list, mid_list, '전체')


if __name__ == '__main__':
  print('crawling.py main 실행')

  conn = pymysql.connect(
    host = 'localhost', # 로컬호스트
    user = 'root',  # 유저
    password = '',  # 비밀번호
    db = 'MEKI',  # 데이터베이스
    charset = 'utf8'  # 인코딩 캐릭터셋
  )
  cursors = conn.cursor()
  print('DB 연동 완료')

  load_cat_list()  
  driver.quit()

else:
  print('crawling.py is imported')