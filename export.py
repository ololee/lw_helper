from importlib.metadata import distributions

# 获取所有已安装的包及其版本
packages = {pkg.metadata['Name']: pkg.version for pkg in distributions()}

out = ""

def sprint(text):
    global out
    out += text + "\n"

  
# 按包名排序并输出
for name, version in sorted(packages.items()):
    sprint(f"{name}=={version}")

with open('requirements.txt', 'w') as f:
    f.write(out)