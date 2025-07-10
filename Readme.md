# lw开发者工具箱
> 本工具包含了数据库操作，gm工具，表格读写工具
## 安装依赖
> pip install -r requirements.txt
## 使用方法
> 先安装依赖，然后执行run.bat
> 程序会启动一个local server,其端口为5000
> 访问http://127.0.0.1:5000/
> 慎用reset_db 功能,会真的重置数据库
## 配置文件
database下的mysql_conf.py里面配置的是sql的脚本，配置好后可以使用reset_db功能

## 二次开发
> 在类前使用装饰器功能可以方便的调用单例&数据解析的local_config装饰器，会自动解析相关的配置文件，
> 数据解析使用了工厂模式，会自动调用对应的解析器
> 在app.py中定义了路由，相应html的请求
> test是生成一些所需的数据
> static 是一些静态文件
> decompile是将来做lw解密的时候用到的，将来还会有个注入的文件夹
> controller 是控制器，用以控制数据的获取和返回
> database 是数据库操作