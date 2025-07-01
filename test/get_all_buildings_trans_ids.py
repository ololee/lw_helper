from config_reader import read_model_config
import json

buildings = read_model_config("../static/config/csv/building.csv")
local_languages = read_model_config("../static/config/txt/Dialog.txt","txt").replace("\ufeff","").strip().split("\n")
trans_set = set()
for building in buildings:
    trans_set.add(building["name"])
    trans_set.add(building["description"])
    trans_set.add(building["long_description"])

langMap = dict()

line = 1
for language in local_languages:
    splits = language.split("=")
    langMap[splits[0]] = splits[1]
    line+=1


out_json_obj = {}
for s in trans_set:
    if s == "":
        continue
    try:
        out_json_obj[s] = langMap[s]
    except Exception as e:
        out_json_obj[s] = s
        print(s)
out_json = json.dumps(out_json_obj,ensure_ascii=False,indent=4)
with open("../static/config/json/building_trans.json","w",encoding="utf-8") as f:
    f.write(out_json)

