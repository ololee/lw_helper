from config_reader import read_model_config
import json

quests = read_model_config("../static/config/csv/quest.csv")
building_cfgs = read_model_config("../static/config/csv/building.csv")
local_languages = read_model_config("../static/config/txt/Dialog.txt","txt").replace("\ufeff","").strip().split("\n")
building_map = dict()
for building in building_cfgs:
    building_map[building["id"]] = building["name"]


building_trans = dict()

trans_set = set()
for quest in quests:
    trans_set.add(quest["name"])
    trans_set.add(quest["desc"])
    paras = []
    para1 = quest["para1"]
    if para1 == "{}" or not "[" in para1:
        if para1 != "{}":
            paras.append(para1)
        else:
            paras = []
    else:
        paras = eval(para1)
    for p in paras:
        if p != 0 and p in building_map:
            building_trans[p] = building_map[p]


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

for s in building_trans:
    if s == "":
        continue
    try:
        out_json_obj[s] = langMap[building_trans[s]]
    except Exception as e:
        out_json_obj[s] = s
        print(s)
out_json = json.dumps(out_json_obj,ensure_ascii=False,indent=4)
with open("../static/config/json/quest_trans.json","w",encoding="utf-8") as f:
    f.write(out_json)

