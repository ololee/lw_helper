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

# 生成 HTML 内容
html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>导航首页</title>
</head>
<body>
    <h1>API 导航</h1>
    <ul>
"""

for route in routes:
    html_content += rf"        <li><a href={route}>{route}</a></li>"

html_content += """    </ul>
</body>
</html>"""

# 写入 index.html 文件
static_html_path = Path('static') / 'html' / 'index.html'
static_html_path.parent.mkdir(parents=True, exist_ok=True)
with open(static_html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)