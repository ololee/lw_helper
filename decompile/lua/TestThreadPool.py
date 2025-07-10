import multiprocessing as mp
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

logical_cores = mp.cpu_count()
MAX_WORKERS = logical_cores

FILE_LENS = len(all_files)


def chunk_data(data, chunk_size):
    frag_count = len(data) // (chunk_size)
    result = []
    for i in range(0, chunk_size - 1):
        result.append(data[i * frag_count:(i + 1) * frag_count])
    result.append(data[(chunk_size - 1) * frag_count:])
    return result


def process_chunk(chunk):
    for file in tqdm(chunk, desc="处理进度"):
        try:
            result = subprocess.run(["java", "-jar", unluac_jar_path, file], capture_output=True, text=True, check=True)
            realPath = file.replace("normal_luac", "lua_file").replace(".luac", ".lua")
            parent_dir = os.path.dirname(realPath)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
            with open(realPath, "w", encoding="utf-8") as writer:
                writer.write(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"这个文件翻译的时候有问题:{file}")
            print(f"命令执行失败，错误信息：{e.stderr}")


if __name__ == '__main__':
    chunks = chunk_data(all_files, chunk_size=MAX_WORKERS)
    with mp.Pool(processes=MAX_WORKERS) as pool:
        results = pool.map(process_chunk, chunks)

