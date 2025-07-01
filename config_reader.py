from file_parser_factory import FileParserFactory
from constants.Cfgs import config_files

def read_model_config(config_path, type=None):
    try:
        return FileParserFactory.get_parser(config_path, type)
    except FileNotFoundError:
        print(f'配置文件 {config_path} 未找到')
        return None


def local_config(configs):
    def decorator(cls):
        original_init = cls.__init__
        def new_init(self,*args, **kwargs):
            if original_init is not object.__init__:
                original_init(self, *args, **kwargs)
            for cfg in configs:
                setattr(self, cfg, read_model_config(config_files[cfg]))
        cls.__init__ = new_init
        return cls
    return decorator

    
