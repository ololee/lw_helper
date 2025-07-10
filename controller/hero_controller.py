from constants.Cfgs import ConfigType
from singleton import singleton
from config_reader import local_config

@singleton
@local_config([ConfigType.building_cfgs,ConfigType.building_trans])
class HeroController():

    def __init__(self):
        pass