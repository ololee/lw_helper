import os

def read7BitEncodedInt(data_buffer, offset):
    result = 0
    offset_len = 0
    bits_read = 0
    while True:
        if bits_read >= 35:
            raise ValueError("Invalid 7-bit encoded integer.")
        byte = data_buffer[offset]
        offset += 1
        offset_len += 1
        result |= (byte & 0x7F) << bits_read
        bits_read += 7
        if (byte & 0x80) == 0:
            break
    return {
        "offset_len": offset_len,
        "content_length": result
    }

def extractFiles(script_file,callback):
    with open(script_file, 'rb') as f:
        data_buffer = f.read()

    offset = 0
    # 读取第一个 32 位整数（忽略）
    offset += 4
    # 读取第二个 32 位整数（忽略）
    offset += 4
    # 读取版本号
    version = int.from_bytes(data_buffer[offset:offset+4], byteorder='little')
    offset += 4
    # 读取文件数量
    count = int.from_bytes(data_buffer[offset:offset+4], byteorder='little')
    offset += 4

    for i in range(count):
        encode_info = read7BitEncodedInt(data_buffer, offset)
        offset += encode_info["offset_len"]
        name_length = encode_info["content_length"]
        name = data_buffer[offset:offset+name_length].decode('utf-8')
        offset += name_length

        content_length = int.from_bytes(data_buffer[offset:offset+4], byteorder='little')
        offset += 4

        content = data_buffer[offset:offset+content_length]
        offset += content_length

        save_file_name = os.path.join("export", name)
        directory = os.path.dirname(save_file_name)
        os.makedirs(directory, exist_ok=True)
        with open(save_file_name, 'wb') as out_file:
            out_file.write(content)
        callback(i,name,count)
    callback(count,"完成",count)


