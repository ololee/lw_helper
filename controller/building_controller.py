from constants.Cfgs import ConfigType
from singleton import singleton
from config_reader import local_config

@singleton
@local_config([ConfigType.building_cfgs,ConfigType.building_trans])
class BuildingController:

    def renderOne(self,buildingCfgItem):
        building = {
            "id":buildingCfgItem["id"],
            "name":self.building_trans[buildingCfgItem["name"]],
            "pic":buildingCfgItem["pic"]
        }
        return building
    def getAll(self):
        renderer_list = []
        map = dict()
        for buildingCfgItem in self.building_cfgs:
            int_id = int(buildingCfgItem["id"])
            id_parent = int_id//1000
            if id_parent in map:
                map[id_parent].append(self.renderOne(buildingCfgItem))
            else:
                map[id_parent] = [self.renderOne(buildingCfgItem)]
        
        for id_parent,building_list in map.items():
            renderer_list.append({
                "id":id_parent * 1000,
                "name":building_list[0]["name"] ,
                "children":building_list,
                "icon":rf"buildings/{building_list[0]["pic"]}"
            })
        return renderer_list

    def getById(self,id):
        ret = {}
        for cfg in self.building_cfgs:
            if cfg["id"] == id:
                ret = cfg
                break
        return ret