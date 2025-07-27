
export_path = rf"Z:\utils\A_Glimpse_lastwar\LuaInject\LuaInject\export"

normal_luac_path = r"Z:\utils\A_Glimpse_lastwar\LuaInject\LuaInject\normal_luac"

import os
from decompile.lua.XLuac2NormalLuac import xlua2NormalLua


all_files = []
for root,dir,files  in os.walk(export_path):
    for file in files:
        abs_path = os.path.join(root,file)
        all_files.append(abs_path)


def GetNormalLuaC(file_path):
    realtive_path = file_path.replace("export","normal_luac")
    with open(file_path,'rb') as reader:
        all_bytes = reader.read()
        normal_lua_bytes = xlua2NormalLua(all_bytes)
        parent_dir = os.path.dirname(realtive_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        with open(realtive_path,'wb') as writer:
            writer.write(normal_lua_bytes)

for file in all_files:
    GetNormalLuaC(file)

