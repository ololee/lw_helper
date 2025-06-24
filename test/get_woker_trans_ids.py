from config_reader import read_model_config
import json

workers = read_model_config("../static/config/csv/lw_worker.csv")
local_languages = read_model_config("../static/config/txt/Dialog.txt","txt").replace("\ufeff","").strip().split("\n")
trans_set = set()
for worker in workers:
    trans_set.add(worker["first_name"])
    trans_set.add(worker["last_name"])

langMap = dict()

line = 1
for language in local_languages:
    splits = language.split("=")
    langMap[splits[0]] = splits[1]
    line+=1


out_json_obj = {}
for s in trans_set:
    out_json_obj[s]= langMap[s]
out_json = json.dumps(out_json_obj,ensure_ascii=False,indent=4)
with open("../static/config/json/worker_trans.json","w",encoding="utf-8") as f:
    f.write(out_json)

