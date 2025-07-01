def mysql_config(config):
    def decorator(cls):
        original_init = cls.__init__
        def new_init(self,*args, **kwargs):
            if original_init is not object.__init__:
                original_init(self, *args, **kwargs)
            setattr(self, "cfg",config)
        cls.__init__ = new_init
        return cls
    return decorator