import pymysql.cursors

conn = pymysql.connect(
    host = '3.34.117.216', # 로컬호스트
    user = 'dayang',  # 유저
    password = 'dayang',  # 비밀번호
    db = 'test',  # 데이터베이스
    charset = 'utf8'  # 인코딩 캐릭터셋
  )

cursors = conn.cursor()
print('DB 연동 완료')

result = []


# item_option 테이블에서 item_id가 같은 요소들의 합을 구해서 item.stock_quantity 수량 바꾸기
try:
  for i in range(1,307):
    result = 0
    cursors.execute("select sum(stock_quantity) from item_option where item_id = " + str(i) +";")
    conn.commit()
    item_stock_quantity_tuple = cursors.fetchone()
    if item_stock_quantity_tuple[0] != None:
      print("진입")
      item_stock_quantity = item_stock_quantity_tuple[0]
      sql = 'update item set stock_quantity =  %s where item_id = %s;' %(str(item_stock_quantity),str(i))
      cursors.execute(sql)
      conn.commit()
      print(item_stock_quantity)
    else:
      continue
   
except:
  print(str(i)+ "번째에서 실패")

print("done")

