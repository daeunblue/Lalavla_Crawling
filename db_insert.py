
# sqls = []

sql.append("insert into Brand(brand_id, brand_name, brand_img) \
    values (%d, %s, %s);") % (brand_id, brand_name, brand_img)

import json

# json file load
with open(/Users/gimda-eun/Lalavla/Lalavla-Crawling/data/brand.json) as json_file:
    json_data = json.load(json_file)

brand_name = json_data[]
brand_id = 
brand_img =

print(json_data[0][0])