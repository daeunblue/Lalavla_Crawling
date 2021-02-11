import os
import sys
import json
from collections import OrderedDict
from time import sleep
from selenium import webdriver

data = OrderedDict()

beauty_list = {
  'skincare': {
    'facial_care': {
      'skin_toner': '1000001000100010001',
      'lotion': '1000001000100010002',
      'essence_serum': '1000001000100010003',
      'cream': '1000001000100010004',
      'mist_fixer': '1000001000100010005',
      'faceoil': '1000001000100010006',
      'eyecream_spotcare': '1000001000100010007',
      'men_allinone': '1000001000100010008',
      'planningset': '1000001000100010009',
      'ample': '1000001000100010011'
    },
    'cleansing': {
      'soap': '1000001000100060002',
      'peeling_scrub': '1000001000100060003',
      'lip_eye_remover': '1000001000100060004',
      'cream_milk': '1000001000100060005',
      'pad_tissue': '1000001000100060006',
      'water': '1000001000100060007',
      'oil_balm': '1000001000100060008',
      'foam_gel': '1000001000100060009'
    },
    'mask': {
      'sheet': '1000001000100020001',
      'washoff': '1000001000100020002',
      'nose': '1000001000100020003',
      'patch': '1000001000100020004',
      'sleeping': '1000001000100020006',
      'modeling': '1000001000100020007',
      'pad_part': '1000001000100020008'
    },
    'suncare': {
      'stick_cushion': '1000001000100070001',
      'tanning_aftersun': '1000001000100070002',
      'cream_lotion': '1000001000100070003',
      'baby_kids': '1000001000100070004',
      'etc': '1000001000100070005'
    }
  },
  'thermocosmetic': {
    'skincare': {
      'mask': '1000001000800070001',
      'faceoil': '1000001000800070002',
      'eyecare': '1000001000800070003',
      'cream': '1000001000800070005',
      'lotion': '1000001000800070006',
      'essence_serum_ample': '1000001000800070007',
      'mist': '1000001000800070008',
      'skin_toner': '1000001000800070009',
      'planningset': '1000001000800070010'
    },
    'cleansing': {
      'lip_eye_remover': '1000001000800060002',
      'peeling_scrub': '1000001000800060003',
      'oil_milk': '1000001000800060004',
      'foam_gel': '1000001000800060005',
      'water': '1000001000800060006'
    },
    'suncare': {
      'stick': '1000001000800050003',
      'cream_lotion': '1000001000800050004'
    },
    'bodycare': {
      'deodorant': '1000001000800040001',
      'femininewash': '1000001000800040002',
      'lipcare': '1000001000800040003',
      'handcream': '1000001000800040004',
      'lotion_cream_oil': '1000001000800040005',
      'wash': '1000001000800040006'
    }
  },
  'makeup': {
    'base': {
      'bb_cc': '1000001000200010001',
      'foundation': '1000001000200010002',
      'primer_base': '1000001000200010003',
      'powder_pact': '1000001000200010004',
      'concealer': '1000001000200010005',
      'blusher_chic': '1000001000200010006',
      'shading_contouring': '1000001000200010007',
      'highlighter': '1000001000200010008',
      'cushion': '1000001000200010009',
      'fixer': '1000001000200010010'
    },
    'nail': {
      'normal': '1000001000200080001',
      'gel': '1000001000200080002',
      'tip_sticker': '1000001000200080003',
      'peditip_sticker': '1000001000200080004',
      'remover': '1000001000200080005',
      'care': '1000001000200080006'
    },
    'lip': {
      'balm': '1000001000200060001',
      'gloss': '1000001000200060002',
      'tint': '1000001000200060003',
      'stick': '1000001000200060004',
      'liner': '1000001000200060005'
    },
    'eye': {
      'mascara': '1000001000200070001',
      'liner': '1000001000200070002',
      'shadow_palette': '1000001000200070003',
      'brow': '1000001000200070004',
      'set': '1000001000200070005'
    }
  },
  'bodycare': {
    'lotion_cream': {
      'lotion': '1000001000300040001',
      'cream': '1000001000300040002',
      'powder': '1000001000300040004'
    },
    'wash_scrub': {
      'bodycleanser': '1000001000300050001',
      'bodyscrub': '1000001000300050002',
      'bathbomb': '1000001000300050003',
      'soap': '1000001000300050004'
    },
    'mist_oil': {
      'bodyoil': '1000001000300060001',
      'bodymist': '1000001000300060002'
    },
    'hand_foot': {
      'handcream': '1000001000300070001',
      'handmask': '1000001000300070002',
      'handwash': '1000001000300070003',
      'planningset': '1000001000300070004',
      'foot_moisturizer': '1000001000300070005',
      'foot_cleanser': '1000001000300070006',
      'foot_recover': '1000001000300070007',
      'pedi_nutritioner': '1000001000300070008',
      'foot_skincell': '1000001000300070009',
      'foot_odor': '1000001000300070010'
    },
    'lipcare': {
      'stick': '1000001000300080001',
      'tube': '1000001000300080002',
      'balm': '1000001000300080003'
    },
    'deo_waxing': {
      'deospray': '1000001000300090001',
      'deostick': '1000001000300090002',
      'deorollon': '1000001000300090003',
      'deotissue': '1000001000300090004',
      'shavingcream_gel': '1000001000300090005',
      'waxcream_strip': '1000001000300090006',
      'shaver': '1000001000300090007',
      'razor': '1000001000300090008'
    }
  },
  'haircare': {
    'shampoo_rinse': {
      'shampoo': '1000001000400080001',
      'rinse_conditioner': '1000001000400080002',
      'planningset': '1000001000400080003'
    },
    'treatment_pack': {
      'hairtreatment': '1000001000400070001',
      'hairpack': '1000001000400070002'
    },
    'styling_essence': {
      'hairessence': '1000001000400060001',
      'hairoil': '1000001000400060002',
      'hairmousse': '1000001000400060003',
      'hairspray': '1000001000400060004',
      'harigel': '1000001000400060005',
      'hairwax': '1000001000400060006',
      'pomade': '1000001000400060007',
      'coating': '1000001000400060008',
      'hairgoods': '1000001000400060009'
    },
    'dye_perm_coating': {
      'perm_coating': '1000001000400050002',
      'fashion_dye': '1000001000400050003',
      'gray_dye': '1000001000400050004'
    },
    'hairgoods': {
      'dryer': '1000001000400040003',
      'straight': '1000001000400040004',
      'setting': '1000001000400040005'
    },
    'hairbrush': {
      'hair': '1000001000400090001'
    }
  },
  'perfume_diffuser': {
    'womenperfume': {
      'women': '1000001000500030001',
      'etc': '1000001000500030002'
    },
    'menperfume': {
      'men': '1000001000500040001'
    },
    'candle_diffuser': {
      'candle': '1000001000500020001',
      'diffuser': '1000001000500020002'
    }
  },
  'beautytool': {
    'face': {
      'eyebrow': '1000001000600010001',
      'curler': '1000001000600010002',
      'eyelashes': '1000001000600010003',
      'doubleeyelid': '1000001000600010004',
      'puff': '1000001000600010005',
      'sponge': '1000001000600010006',
      'makeupbrush': '1000001000600010007',
      'oilfilm': '1000001000600010008'
    },
    'hair': {
      'tool': '1000001000600020001',
      'brush': '1000001000600020002',
      'accessory': '1000001000600020003'
    },
    'nail': {
      'care_art': '1000001000600030001'
    },
    'appliance': {
      'cleansing': '1000001000600040001',
      'massage': '1000001000600040002',
      'nail': '1000001000600040003'
    },
    'etc': {
      'cottonswab': '1000001000600050001',
      'cottonpad': '1000001000600050002',
      'bottle': '1000001000600050003',
      'maskready': '1000001000600050004',
      'cleansingready': '1000001000600050005',
      'etc': '1000001000600050006'
    }
  },
  'men': {
    'skincare': {
      'allinone': '1000001000700070006',
      'toner_lotion': '1000001000700070007',
      'essence_cream': '1000001000700070008',
      'sun_mask_cleansing': '1000001000700070009',
      'set': '1000001000700070010'
    },
    'makeup': {
      'bb_cc': '1000001000700080003',
      'cushion_pact': '1000001000700080004',
      'concealer': '1000001000700080005',
      'lip_eye': '1000001000700080006'
    },
    'haircare': {
      'wax': '1000001000700090001',
      'pomade': '1000001000700090002',
      'gel_mousse': '1000001000700090003',
      'essence_cream': '1000001000700090004',
      'spray': '1000001000700090005',
      'haircleanse': '1000001000700090006',
      'dye_perm': '1000001000700090007',
      'makeup': '1000001000700090008',
      'tool': '1000001000700090009'
    },
    'shaving': {
      'electric': '1000001000700100002',
      'foam_gel_oil_cream': '1000001000700100003',
      'aftershave': '1000001000700100004'
    },
    'bodycare': {
      'lip_hand_foot': '1000001000700110001',
      'deo_wax': '1000001000700110002',
      'bodyperfume': '1000001000700110003',
      'wash_sanitizer': '1000001000700110004'
    },
    'perfume': {
      'perfume': '1000001000700120001'
    },
    'tool_etc': {
      'tool': '1000001000700130001',
      'underwear_fashion': '1000001000700130002',
      'etc_hobby': '1000001000700130003'
    },
    'health_exercise': {
      'healthfood': '1000001000700140001',
      'exercise_medical': '1000001000700140002'
    }
  }
}

health_food_list = {
  'health_hygeine': {
    'dentalcare': {
      'toothbrush': '1000002000300010001',
      'toothpaste': '1000002000300010002',
      'electric': '1000002000300010003',
      'floss': '1000002000300010004',
      'toothwhitening': '1000002000300010005',
      'toothhygeine': '1000002000300010006',
      'sterilizer': '1000002000300010007',
      'tripset': '1000002000300010008' 
    },
    'eyecare': {
      'lenscare': '1000002000300020001',
      'lenssterilizer': '1000002000300020002',
      'eyemask': '1000002000300020003'
    },
    'women_hygeine': {
      'femininewash': '1000002000300030001',
      'sanitarypad': '1000002000300030003',
      'pantyliner': '1000002000300030004',
      'tampon': '1000002000300030005',
      'diaper': '1000002000300030006'
    },
    'health_massage': {
      'health': '1000002000300060001',
      'supplement': '1000002000300060002',
      'yoga_pilates': '1000002000300060003',
      'sportswear': '1000002000300060004',
      'correction': '1000002000300060005',
      'massage': '1000002000300060006'
    },
    'spotpatch_medical': {
      'spotpatch': '1000002000300050004',
      'bandaid': '1000002000300050005',
      'mask': '1000002000300050006',
      'muscle': '1000002000300050008',
      'adult': '1000002000300050010',
      'bug': '1000002000300050012'
    }
  },
  'healthfood': {
    'vitamin': {
      'complex': '1000002000100060001',
      'c': '1000002000100060002',
      'b': '1000002000100060003',
      'd': '1000002000100060004'
    },
    'lacto': {
      'probiotics': '1000002000100070001',
      'prebiotics': '1000002000100070002',
      'synbiotics': '1000002000100070003',
      'feminine': '1000002000100070004'
    },
    'iron_folate_cal': {
      'propolis': '1000002000100080001',
      'folate': '1000002000100080002',
      'iron_cal_mag': '1000002000100080003'
    },
    'blood_eye_liver': {
      'milkthistle': '1000002000100090001',
      'lutein': '1000002000100090002',
      'omega3': '1000002000100090003',
      'gamma': '1000002000100090004',
      'krilloil': '1000002000100090005'
    },
    'diet_beauty_health': {
      'collagen_hyal': '1000002000100100001',
      'slimming': '1000002000100100002'
    },
    'ginseng_drink': {
      'ginsengstick': '1000002000100110001',
      'ginsengdrink': '1000002000100110003',
      'healthjuice': '1000002000100110004',
      'sunsik_etc': '1000002000100110006'
    },
    'kids_health': {
      'vitamin': '1000002000100120001',
      'ginseng': '1000002000100120002',
      'omega3': '1000002000100120003',
      'lacto': '1000002000100120004',
      'cal_propolis': '1000002000100120005'
    },
    'giftset': {
      'giftset': '1000002000100130001'
    },
    'etc_food': {
      'etc': '1000002000100140001'
    }
  },
  'normalfood': {
    'dessert_snack': {
      'bakery_ricecake': '1000002000200180001',
      'snack': '1000002000200180002',
      'nuts': '1000002000200180003',
      'chocolate': '1000002000200180004',
      'candy_jelly_gum': '1000002000200180005',
      'icecream': '1000002000200180006'
    },
    'water_drink_dairy': {
      'water_sparkle': '1000002000200170001',
      'dairy': '1000002000200170002',
      'coffee_tea': '1000002000200170003',
      'juice': '1000002000200170004',
      'drink': '1000002000200170005'
    },
    'coffee_tea': {
      'coffee': '1000002000200160001',
      'tea': '1000002000200160002'
    },
    'processedfood': {
      'rice': '1000002000200190001',
      'salad_lunch': '1000002000200190002',
      'chickenbreast': '1000002000200190003',
      'sunsik_cereal_granola': '1000002000200190004',
      'noodle': '1000002000200190005',
      'frozen': '1000002000200190006',
      'jjigae_side': '1000002000200190007',
      'soup_sauce': '1000002000200190008'
    },
    'kidsfood': {
      'powderedmilk': '1000002000200150001',
      'kidssnack': '1000002000200150002',
      'kidsdrink': '1000002000200150003'
    },
    'giftset': {
      'giftset': '1000002000200140001'
    }
  }
}

life_list = {
  'pet': {
    'dogfood': {
      'health_food': '1000003000300010001',
      'snack': '1000003000300010002',
      'feed': '1000003000300010003'
    },
    'doggoods': {
      'outing': '1000003000300020001',
      'fashion': '1000003000300020002',
      'house': '1000003000300020003',
      'toy': '1000003000300020004',
      'beauty': '1000003000300020005',
      'bath': '1000003000300020006',
      'plate_bottle': '1000003000300020007',
      'bowel_hygeine': '1000003000300020008'
    },
    'catfood': {
      'feed': '1000003000300030001',
      'can_snack': '1000003000300030002',
      'health_food': '1000003000300030003'
    },
    'catgoods': {
      'sand_hygeine': '1000003000300040001',
      'bath': '1000003000300040003',
      'beauty': '1000003000300040004',
      'toy': '1000003000300040005',
      'house': '1000003000300040006'
    }
  },
  'baby': {
    'skin_bodycare': {
      'suncream_suncare': '1000003000400010001',
      'shampoo_rinse': '1000003000400010002',
      'balm_lipcare': '1000003000400010003',
      'bath_oil': '1000003000400010004',
      'lotion_cream': '1000003000400010005'
    }
  },
  'diaper_watertissue': {
    'watertissue': '1000003000400020001',
    'diaper': '1000003000400020002'
  },
  'kidsgoods': {
    'procreation': '1000003000400030001',
    'kidsdetergent': '1000003000400030002',
    'lactation': '1000003000400030003',
    'oral_safe': '1000003000400030004'
  },
  'babyfood_snack': {
    'babyfood': '1000003000400040001',
    'drink': '1000003000400040002',
    'babysnack': '1000003000400040003',
    'powderedmilk': '1000003000400040004'
  },
  'etc': {
    'freshener_deodorant': {
      'deodorant': '1000003000200020001',
      'car_freshener': '1000003000200020002'
    },
    'detergent_tissue': {
      'cleandet': '1000003000200100001',
      'kitchendet': '1000003000200100002',
      'bathroom': '1000003000200100003',
      'laundrydet': '1000003000200100005',
      'watertissue': '1000003000200100006',
      'rolltissue': '1000003000200100007',
      'functionaltissue': '1000003000200100008',
      'facialtissue': '1000003000200100009'
    },
    'fashiongoods': {
      'underwear': '1000003000200050001',
      'socks_stocking_leggings': '1000003000200050002',
      'shoemanage': '1000003000200050008',
      'season_fashion': '1000003000200050011'
    },
    'officesupply': {
      'notebook': '1000003000200010001',
      'fancy_office': '1000003000200010003',
      'facny_party': '1000003000200010004',
      'card': '1000003000200010005',
      'battery': '1000003000200010007',
      'character': '1000003000200010008'
    },
    'sound_communicate': {
      'ear_headphone': '1000003000200040001',
      'speaker': '1000003000200040002',
      'phoneacc': '1000003000200040003'
    },
    'homeappliance_digital': {
      'kitchenapp': '1000003000200090001',
      'livingapp': '1000003000200090002',
      'kitchenprop': '1000003000200090003'
    },
    'interior': {
      'interiorprop': '1000003000200120001'
    }
  }
}

goods_list = {
  'beauty_list': beauty_list, 
  'health_food_list': health_food_list, 
  'life_list': life_list
}

url = 'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo='

driver = webdriver.Chrome("C:\\Python38\\chromedriver")

def get_product_info(index, big_list, mid_list, small_list, category):
  # number : 단일 String
  # img : 단일 String (src)
  # brand : 단일 String
  # name : 단일 String
  # score : 단일 String
  # review_count : 단일 String (**건)
  # category_list : String 리스트 
  # is_discount : boolean (할인 여부)
  # discount_price : 단일 String (**원)
  # origin_price : 단일 String (**원)

  # 옵션이 없는 단일 상품의 경우, 옵션 개수를 0개로 할 것인가 1개로 할 것인가
  # 그리고 옵션 이름 목록과 가격에 그냥 name과 price를 넣어야 하나?

  # option_count : 단일 String (옵션 개수)
  # option_name_list : String 리스트 (옵션별 이름)
  # option_price_list : String 리스트 (옵션별 가격)
  # option_img_list : String 리스트 (옵션별 이미지 src)

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