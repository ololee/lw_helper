from config_reader import local_config, read_model_config
from constants.Cfgs import ConfigType
from constants.WorkerCfg import QualityColorCfg
from singleton import singleton


@singleton
@local_config([ConfigType.worker_cfgs,ConfigType.worker_trans,ConfigType.worker_icons])
class WorkerController:

    def renderOne(self,worker):
        id = worker["id"]
        name = self.worker_trans[worker["last_name"]]
        clazz = self.worker_trans[worker["first_name"]]
        icon = self.worker_icons[id]["appearance"]
        trans_goods = worker["trans_goods"]
        [fragId,fragCount] = trans_goods.split(";")
        hero = {
            "id":id,
            "last_name":worker["last_name"],
            "name":name,
            "class":clazz,
            "first_name":worker["first_name"],
            "quality":int(worker["quality"]),
            "background_color":QualityColorCfg[int(worker["quality"])],
            "icon":rf"worker/{icon}.png",
            "frag_id":fragId,
            "frag_count":int(fragCount)
        }
        return hero
    def getALl(self):
         renderer_list = []
         for worker in self.worker_cfgs:
             renderer_list.append(self.renderOne(worker))

         renderer_list.sort(key= lambda p:( -p["quality"],p["class"]) )
         return renderer_list
    
    def filter(self,id,quality,job):
        if id == "":
           renderer_list = []
           for worker in self.worker_cfgs:
               if int(worker["quality"]) == quality:
                   if job == "-1":
                       renderer_list.append(self.renderOne(worker))
                   elif job == worker["first_name"]:
                       renderer_list.append(self.renderOne(worker))
               elif quality == -1:
                   if job == worker["first_name"]:
                       renderer_list.append(self.renderOne(worker))
           renderer_list.sort(key= lambda p:( -p["quality"],p["class"]))
           return renderer_list
        else:   
            for worker in self.worker_cfgs:
                if worker["id"] == id:
                    return [self.renderOne(worker)]
