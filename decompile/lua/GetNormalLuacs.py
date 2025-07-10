
export_path = rf"Z:\utils\A_Glimpse_lastwar\LuaInject\LuaInject\export"

normal_luac_path = r"Z:\utils\A_Glimpse_lastwar\LuaInject\LuaInject\normal_luac"

import os


all_files = []
for root,dir,files  in os.walk(export_path):
    for file in files:
        abs_path = os.path.join(root,file)
        all_files.append(abs_path)

def xlua2NormalLua(origin: bytes) -> bytes:
    origin_length = len(origin)
    result = bytearray(origin_length + 1)
    # 复制前14字节（索引0-13）
    result[:14] = origin[:14]
    # 修改第6个字节（索引5）为0x00
    result[5] = 0x00
    # 修改第15个字节（索引14）为0x04
    result[14] = 0x04
    # 将原始数据从第15字节开始（索引14）复制到目标数组的16字节位置（索引15）
    result[15:] = origin[14:]
    return bytes(result)


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

