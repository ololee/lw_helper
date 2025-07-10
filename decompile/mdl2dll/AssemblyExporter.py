import os
import sys
import stat
from pathlib import Path

new_extension = '.dll'
header_bytes = bytes([0x4D, 0x5A, 0x90, 0x00, 0x03, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xB8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

def ask_for_directories():
    source_dir = input('请输入源目录: ')
    target_dir = input('请输入目标目录: ')
    
    # 开始处理
    target_path = Path(target_dir)
    if not target_path.exists():
        target_path.mkdir(parents=True)
    
    modify_files(source_dir, target_dir)

def modify_files(source, target):
    try:
        files = os.listdir(source)
    except OSError as err:
        print(f"无法读取目录 {source}:", err)
        return

    for file in files:
        file_path = os.path.join(source, file)
        try:
            stats = os.stat(file_path)
        except OSError as err:
            print(f"无法获取文件信息 {file_path}:", err)
            return

        if stat.S_ISREG(stats.st_mode):
            parts = file.split('.')
            if len(parts) >= 2:
                new_file_name = '.'.join(parts[:-1]) + new_extension
                new_file_path = os.path.join(target, new_file_name)

                try:
                    with open(file_path, 'rb') as f:
                        data = f.read()
                except OSError as err:
                    print(f"无法读取文件 {file_path}:", err)
                    return

                modified_data = header_bytes + data[len(header_bytes):]

                try:
                    with open(new_file_path, 'wb') as f:
                        f.write(modified_data)
                except OSError as err:
                    print(f"无法写入文件 {new_file_path}:", err)
                    return

if __name__ == '__main__':
    ask_for_directories()