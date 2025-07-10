from constants.Cfgs import ConfigType
from singleton import singleton
from config_reader import local_config

@singleton
@local_config([ConfigType.hero_cfgs,ConfigType.hero_trans,ConfigType.hero_appearance_cfgs])
class HeroController():

    def render_appearances(self):
        if not hasattr(self,"appearance_dict"):
            self.appearance_dict = dict()
            for app_cfg in self.hero_appearance_cfgs:
                self.appearance_dict[app_cfg["id"]] = app_cfg
            return self.appearance_dict
        else:
            return self.appearance_dict
        

    def renderOne(self, hero_cfg):
        """
        渲染单个英雄
        """
        id = hero_cfg["id"]
        name = hero_cfg["first_name"]
        hero_trans = self.hero_trans[name]
        appearance = hero_cfg["appearance"]
        appearance_cfg = self.render_appearances()[appearance]
        half_icon = appearance_cfg["half_icon_path"]
        return {
            "id": id,
            "name": hero_trans,
            "icon": rf"hero/{half_icon}.png"
        }

    def getAll(self):
        """
        获取所有英雄
        """
        renderer_list = []
        for hero_cfg in self.hero_cfgs:
            renderer_list.append(self.renderOne(hero_cfg))
        return renderer_list

    def getHeroCfgDict(self):
        if not hasattr(self,"hero_dict"):
            self.hero_dict = dict()
            for hero_cfg in self.hero_cfgs:
                self.hero_dict[hero_cfg["id"]] = hero_cfg
        return self.hero_dict
    def filter(self,id,quality,isHuman,onlyList):
        print(id,quality,isHuman,onlyList)
        mdict = self.getHeroCfgDict()
        if id != "":
            cfg = mdict[id]
            return [self.renderOne(cfg)]
        if isHuman == "-1":
            pass
        elif isHuman == "1":
            mdict = {k:v for k,v in mdict.items() if v["is_human"] == "1"}
        else:
            mdict = {k:v for k,v in mdict.items() if v["is_human"] == "0"}
        
        if onlyList == "-1":
            pass
        elif onlyList == "1":
            mdict = {k:v for k,v in mdict.items() if v["display_in_hero_list"] == "1"}
        return [self.renderOne(cfg) for k,cfg in mdict.items() ]
        