def luac2XLuac(origin: bytes) -> bytes:
    origin_length = len(origin)
    result = bytearray(origin_length - 1)
    result[:14] = origin[:14]
    result[5] = 0x01
    result[14:] = origin[15:]
    return bytes(result)