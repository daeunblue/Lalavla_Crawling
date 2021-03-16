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
driver.implicitly_wait(5)

def execute_sql(sqls):
  with open('sql_abc.txt', 'a') as f:
    f.writelines(sqls)


  # for sql in sqls:
  #   print(sql)
  #   cursors.execute(sql)
  #   conn.commit()

# DB 연동
conn = pymysql.connect(
  host = 'localhost', # 로컬호스트
  user = 'root',  # 유저
  password = '',  # 비밀번호
  db = 'MEKI',  # 데이터베이스
  charset = 'utf8'  # 인코딩 캐릭터셋
)
cursors = conn.cursor()
print('DB 연동 완료')



# 네비게이션 바에서 ㄱ~ㅎ, ABC까지 하나씩 탭하기
brand_btn_lists = driver.find_elements_by_class_name('nav-brdSrch > li')  # ㄱ~ABC
count = 1 # 전체 브랜드 개수
brand_dict = dict()


# ㄱ~ㅎ, ABC까지 버튼이 ch_btn에 들어감
for i in range(14,15):
  sqls = []
  
  brand_btn_lists[i].click()  # 첨자 버튼 클릭
  sleep(0.3)
  driver.implicitly_wait(3)
  # 전체보기 버튼 밑의 브랜드 리스트들
  brand_lists = driver.find_elements_by_class_name('list-brdSrchResult > li a')
  ch_brand_count = len(brand_lists) # 해당 첨자의 브랜드 개수들

  for k in range(ch_brand_count):
    # staleElement 에러 때문에 매번 새로 찾아줘야 함
    brand_lists = driver.find_elements_by_class_name('list-brdSrchResult > li a')
    brand = brand_lists[k]
    driver.implicitly_wait(3)
    b_name = brand.text
    brand.click() # 각 브랜드를 클릭해 들어가기
    driver.implicitly_wait(3)

    try:
      # 브랜드 이미지 찾기
      brand_img = (driver.find_element_by_id("topvisual-image")).get_attribute('src')
      if brand_img == 'http://mimg.lalavla.com/resources':  # 이미지가 없을 경우 except 절로
        raise Exception                  
      brand_dict[b_name] = [count, str(brand_img)]
    except: # 이미지가 없을 경우
      brand_dict[b_name] = [count, "X"]

    # print("브랜드이름 :"+ b_name)
    # print("src: "+str(brand_dict[b_name][1]))
   
    count += 1  # 브랜드 1개 찾았으니 count 증가
    driver.back()
    driver.implicitly_wait(3)
    
    # insert sql
    sqls.append("insert into Brand(brand_name, brand_img) \
      values ('%s', '%s'); \n" % (str(b_name), str(brand_dict[b_name][1])))
    
  # excute sql
  execute_sql(sqls)

  brand_btn_lists = driver.find_elements_by_class_name('nav-brdSrch > li')  # ㄱ~ABC
  sleep(0.5)
  driver.implicitly_wait(3)


driver.quit()




# try:
#   with open(
#     './data/brand.json', 'w', encoding='utf-8') as f:
#     json.dump(brand_dict, f, ensure_ascii=False, indent="\t")
# except: # 디렉터리가 없을 때만 디렉터리를 만듦
#   os.makedirs('./data')

print('done!')