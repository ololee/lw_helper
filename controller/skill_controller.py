from constants.Cfgs import ConfigType
from singleton import singleton
from config_reader import local_config
import json

@singleton
@local_config([ConfigType.skill_cfgs,ConfigType.skill_trans])
class SkillController:
    

    def renderOne(self,skill):
        return skill
    
    def getALl(self):
        renderer_list = []
        for skill in self.skill_cfgs:
            renderer_list.append(self.renderOne(skill))
        return renderer_list