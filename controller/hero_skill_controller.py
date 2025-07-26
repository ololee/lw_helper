from constants.Cfgs import ConfigType
from singleton import singleton
from config_reader import local_config
import json

@singleton
@local_config([ConfigType.hero_skill_cfgs,ConfigType.hero_skill_trans])
class HeroSkillController:
    

    def renderOne(self,skill):
        name_id = skill["name"]
        name = name_id
        if name_id in self.hero_skill_trans:
            name = self.hero_skill_trans[name_id]
        icon = skill["icon"]
        icon = icon.replace("Assets/Main/Sprites/","static/icons/hero_skills/")
        return {
            "id":skill["id"],
            "name":name,
            "icon":icon
        }
    
    def getALl(self):
        renderer_list = []
        for skill in self.hero_skill_cfgs:
            renderer_list.append(self.renderOne(skill))
        return renderer_list