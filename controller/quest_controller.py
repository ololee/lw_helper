from constants.Cfgs import ConfigType
from singleton import singleton
from config_reader import local_config
import json

@singleton
@local_config([ConfigType.quest_trans,ConfigType.quest_cfgs])
class QuestController:

    def renderOne(self,cfg):
        name = cfg["name"]
        trans_name = ""
        desc = cfg["desc"]
        if not (name == "" or name == ''):
            trans_name = self.quest_trans[name]
        desc_trans = ""
        if desc != "":
            desc_trans = self.quest_trans[desc]
        para1 = cfg["para1"]
        para2 = cfg["para2"]
        para1_trans = []
        if para1 != "":
            para1_ev = eval(para1)
            if type(para1_ev) == list:
                p0 = para1_ev[0]
                if p0 in self.quest_trans:
                    para1_trans.append(self.quest_trans[p0])
                else:
                    para1_trans.append(p0)
            para1_trans.append(para2)
        return {
            "id": cfg["id"],
            "name":trans_name ,
            "pic":"",
            "desc":desc_trans + "--" + json.dumps(para1_trans,ensure_ascii=False),
            "id":cfg["id"]
        }

    def getAll(self):
        render_list = []
        for cfg in self.quest_cfgs:
            render_list.append(self.renderOne(cfg))
        render_list.sort(key= lambda p:p["id"])
        return render_list

    def mapCfgs2Map(self):
        ret = dict()
        for cfg in self.quest_cfgs:
            ret[cfg["id"]] = cfg
        return ret

    def getChapterCSV(self):
        csv_data = []
        length = 40
        amap = self.mapCfgs2Map()
        for i in range(length):
            quest_id = f"10001{i+1:02d}"
            quest_cfg = amap[quest_id]
            item = self.renderOne(quest_cfg)
            csv_data.append([quest_id, item["name"], item["desc"]])
        return csv_data


