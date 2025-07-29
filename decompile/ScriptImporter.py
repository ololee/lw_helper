import os
import struct
import zlib
from io import BytesIO


def get_all_files(dir_path):
    file_list = []
    directory_list = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_list.append(full_path)
        for dir in dirs:
            directory_list.append(os.path.join(root, dir))

    return file_list


def write_7bit_encoded_int(buffer_array, value):
    while value >= 0x80:
        buffer_array.append(bytes([value | 0x80]))
        value >>= 7
    buffer_array.append(bytes([value]))


def write_binary_string(buffer_array, string):
    encoded_string = string.encode('utf-8')
    write_7bit_encoded_int(buffer_array, len(encoded_string))
    buffer_array.append(encoded_string)


def create_binary_file(input_dir, input_binary_file, output_binary_file,progress_callback):
    with open(input_binary_file, 'rb') as file:
        data_buffer = file.read()

    buffer_array = []
    magic = struct.unpack('<I', data_buffer[0:4])[0]
    tmp_val = struct.unpack('<I', data_buffer[4:8])[0]
    version = struct.unpack('<I', data_buffer[8:12])[0]

    file_list = get_all_files(input_dir)

    header_buffer = struct.pack('<III', magic, tmp_val, version)
    buffer_array.append(header_buffer)

    file_count_buffer = struct.pack('<I', len(file_list))
    buffer_array.append(file_count_buffer)

    count = 0
    total = len(file_list)
    for file_path in file_list:
        file_name = os.path.relpath(file_path, input_dir)
        file_name = file_name.replace(os.sep, '/')

        with open(file_path, 'rb') as f:
            file_content = f.read()

        write_binary_string(buffer_array, file_name)

        content_length_buffer = struct.pack('<I', len(file_content))
        buffer_array.append(content_length_buffer)

        buffer_array.append(file_content)

        if count % 50 == 0:
            progress_callback(count,file_path,total)
        count += 1
    
    progress_callback(total,"",total)

    final_buffer = b''.join(buffer_array)

    with open(output_binary_file, 'wb') as out_file:
        out_file.write(final_buffer)

    print(f"Binary file created at: {output_binary_file}")


def create_crc_size_file(output_binary_file, output_crc_file):
    with open(output_binary_file, 'rb') as file:
        data_buffer = file.read()

    length = len(data_buffer)
    buffer_crc32 = zlib.crc32(data_buffer)

    output_content = f"{length}|{buffer_crc32}"
    with open(output_crc_file, 'w') as out_file:
        out_file.write(output_content)

    print(f"Crc32 result exported to: {output_crc_file}")



def compressFiles(input_directory,input_binary_file,output_binary_file,output_crc_file,progress_callback):
    create_binary_file(input_directory, input_binary_file, output_binary_file,progress_callback)
    create_crc_size_file(output_binary_file, output_crc_file)
