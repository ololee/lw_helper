import re
from pathlib import Path


ignores = []

def ignore_route(route):
    pass
    

# 读取 app.py 文件内容
with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

# 使用正则表达式提取带有 @ignore_route 的路由函数名
ignore_pattern = re.compile(r'@ignore_route\s*\n\s*@app.route\((.*?)\)')
ignore_matches = ignore_pattern.findall(app_code)
ignore_routes = [match.strip('"\' ') for match in ignore_matches]

# 使用正则表达式提取路由信息
route_pattern = re.compile(r'@app.route\((.*?)\)')
matches = route_pattern.findall(app_code)

# 解析出路由路径
routes = []
for match in matches:
    route = match.strip('"\' ')
    if route != '/' and route not in ignore_routes:  # 排除首页路由和被忽略的路由
        routes.append(route)
