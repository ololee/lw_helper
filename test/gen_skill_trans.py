from config_reader import read_model_config
import json

skills = read_model_config("../static/config/csv/skill.csv")
local_languages = read_model_config("../static/config/txt/Dialog.txt","txt").replace("\ufeff","").strip().split("\n")
trans_set = set()

def add_setItem(item):
    global trans_set
    if item != None and item != "":
        trans_set.add(item)

for skill in skills:
    # add_setItem(skill["effect_num_des"])
    add_setItem(skill["name"])
    add_setItem(skill["type_des"])

langMap = dict()

line = 1
for language in local_languages:
    splits = language.split("=")
    langMap[splits[0]] = splits[1]
    line+=1


out_json_obj = {}
for s in trans_set:
    if s in langMap:
        out_json_obj[s] = langMap[s]
    else:
        out_json_obj[s] = s
out_json = json.dumps(out_json_obj,ensure_ascii=False,indent=4)
with open("../static/config/json/skill_trans.json","w",encoding="utf-8") as f:
    f.write(out_json)

