class ConfigType:
    worker_cfgs = "worker_cfgs"
    worker_trans = "worker_trans"
    worker_icons = "worker_icons"
    building_cfgs = "building_cfgs"
    building_trans = "building_trans"
    army_cfgs = "army_cfgs"
    army_trans = "army_trans"


config_files = {
    ConfigType.worker_cfgs: "./static/config/csv/lw_worker.csv",
    ConfigType.worker_trans: "./static/config/json/worker_trans.json",
    ConfigType.worker_icons: "./static/config/json/worker_appearance_config.json",
    ConfigType.building_cfgs: "./static/config/csv/building.csv",
    ConfigType.building_trans: "./static/config/json/building_trans.json",
    ConfigType.army_cfgs : "./static/config/csv/lw_army.csv",
    ConfigType.army_trans : "./static/config/json/army_trans.json"
}
