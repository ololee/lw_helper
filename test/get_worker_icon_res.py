from config_reader import read_model_config
import json

workers = read_model_config("../static/config/csv/lw_worker.csv")
hero_appearance = read_model_config("../static/config/csv/lw_hero_appearance.csv")

local_languages = read_model_config("../static/config/txt/Dialog.txt","txt").replace("\ufeff","").strip().split("\n")

id_ap_dict = dict()
app_map = dict()

for appear in hero_appearance:
    app_map[appear['id']] = appear['half_icon_path']

for worker in workers:
    id_ap_dict[worker["id"]]= {
        "id":worker["id"],
        "appearance_id":worker["appearance"],
        "appearance":app_map[worker["appearance"]]
    }

out_json = json.dumps(id_ap_dict,indent=4,ensure_ascii=False)

with open("../static/config/json/worker_appearance_config.json","w",encoding="utf-8") as f:
    f.write(out_json)



