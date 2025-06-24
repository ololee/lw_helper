from file_parser_factory import FileParserFactory


def read_model_config(config_path, type=None):
    try:
        return FileParserFactory.get_parser(config_path, type)
    except FileNotFoundError:
        print(f'配置文件 {config_path} 未找到')
        return None
