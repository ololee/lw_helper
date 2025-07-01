from constants.Cfgs import ConfigType
from singleton import singleton
from config_reader import local_config

@singleton
@local_config([ConfigType.army_cfgs,ConfigType.army_trans])
class ArmyController:

    def renderOne(self,cfg):
        return {
            "id":cfg["id"],
            "icon":cfg["army_icon"],
            "name":self.army_trans[cfg["name"]]
        }
    def getAll(self):
        renderer_list = []
        for cfg in self.army_cfgs:
            renderer_list.append(self.renderOne(cfg))
        return renderer_list