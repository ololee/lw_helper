unluac_jar_path = rf"Z:\tools\xlua_editor\xlua_editor\src\main\resources\unluac_2020_05_28.jar"
from tqdm import tqdm
normal_luac_path = r"Z:\utils\A_Glimpse_lastwar\LuaInject\LuaInject\normal_luac"

import os
import subprocess


all_files = []
for root,dir,files  in os.walk(normal_luac_path):
    for file in files:
        abs_path = os.path.join(root,file)
        all_files.append(abs_path)



for file in tqdm(all_files,desc="处理进度"):
    try:
        result = subprocess.run(["java", "-jar",unluac_jar_path,file], capture_output=True, text=True, check=True)
        realPath = file.replace("normal_luac","lua_file").replace(".luac",".lua")
        parent_dir = os.path.dirname(realPath)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        with open(realPath,"w",encoding="utf-8") as writer:
            writer.write(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"这个文件翻译的时候有问题:{file}")
        print(f"命令执行失败，错误信息：{e.stderr}")