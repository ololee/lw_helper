class ConfigType:
    worker_cfgs = "worker_cfgs"
    worker_trans = "worker_trans"
    worker_icons = "worker_icons"
    building_cfgs = "building_cfgs"
    building_trans = "building_trans"
    army_cfgs = "army_cfgs"
    army_trans = "army_trans"
    quest_cfgs = "quest_cfgs"
    quest_trans = "quest_trans"
    hero_trans = "hero_trans"
    hero_cfgs = "hero_cfgs"
    hero_appearance_cfgs = "hero_appearance_cfgs"
    skill_cfgs = "skill_cfgs"
    skill_trans = "skill_trans"
    hero_skill_cfgs = "hero_skill_cfgs"
    hero_skill_trans = "hero_skill_trans"


config_files = {
    ConfigType.worker_cfgs: "./static/config/csv/lw_worker.csv",
    ConfigType.worker_trans: "./static/config/json/worker_trans.json",
    ConfigType.worker_icons: "./static/config/json/worker_appearance_config.json",
    ConfigType.building_cfgs: "./static/config/csv/building.csv",
    ConfigType.building_trans: "./static/config/json/building_trans.json",
    ConfigType.army_cfgs : "./static/config/csv/lw_army.csv",
    ConfigType.army_trans : "./static/config/json/army_trans.json",
    ConfigType.quest_cfgs : "./static/config/csv/quest.csv",
    ConfigType.quest_trans : "./static/config/json/quest_trans.json",
    ConfigType.hero_cfgs : "./static/config/csv/lw_hero.csv",
    ConfigType.hero_trans : "./static/config/json/hero_trans.json",
    ConfigType.hero_appearance_cfgs : "./static/config/csv/lw_hero_appearance.csv",
    ConfigType.skill_cfgs : "./static/config/csv/skill.csv",
    ConfigType.skill_trans : "./static/config/json/skill_trans.json",
    ConfigType.hero_skill_cfgs: "./static/config/csv/lw_hero_skill.csv",
    ConfigType.hero_skill_trans: "./static/config/json/hero_skill_trans.json"
}
