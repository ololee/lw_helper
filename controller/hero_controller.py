from config_reader import read_model_config
from constants.WorkerCfg import QualityColorCfg
from singleton import SingletonMeta


class HeroController(metaclass=SingletonMeta):

    def __init__(self):
        self.worker_cfgs =  read_model_config('./static/config/csv/lw_worker.csv')
        self.worker_trans = read_model_config("./static/config/json/worker_trans.json")
        self.worker_icons = read_model_config("./static/config/json/worker_appearance_config.json")

    def renderOne(self,worker):
        id = worker["id"]
        name = self.worker_trans[worker["last_name"]]
        clazz = self.worker_trans[worker["first_name"]]
        icon = self.worker_icons[id]["appearance"]
        hero = {
            "id":id,
            "last_name":worker["last_name"],
            "name":name,
            "class":clazz,
            "first_name":worker["first_name"],
            "quality":int(worker["quality"]),
            "background_color":QualityColorCfg[int(worker["quality"])],
            "icon":rf"worker/{icon}.png"
        }
        return hero
    def getALl(self):
         renderer_list = []
         for worker in self.worker_cfgs:
             renderer_list.append(self.renderOne(worker))

         renderer_list.sort(key= lambda p:( -p["quality"],p["class"]) )
         return renderer_list
    
    def getWorkerCfgById(self,id):
        for worker in self.worker_cfgs:
            if worker["id"] == id:
                return self.renderOne(worker)