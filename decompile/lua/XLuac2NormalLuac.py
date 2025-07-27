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