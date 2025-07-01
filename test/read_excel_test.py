import openpyxl
import os
from openpyxl_image_loader import SheetImageLoader

# 打开 Excel 文件
workbook = openpyxl.load_workbook('../static/config/xlsx/monitor.xlsx')
sheet = workbook['广元长虹']  # 替换为你的表名

# 创建图像加载器
image_loader = SheetImageLoader(sheet)

save_dir =  os.path.join(os.getcwd(),"../static/ppt/mosu")

markdown_path = os.path.join(os.getcwd(),"../static/ppt/changhong.txt")

markdown_content = ""
# 遍历单元格查找图片
for row in sheet.iter_rows():
    for cell in row:

        if cell.coordinate.startswith("C") and cell.row >2:
            markdown_content+=f"{cell.value}\n"
        if cell.column == 4 and cell.row > 2:
            markdown_content += f"{cell.value}\n\n"
            # markdown_content += rf"![](mosu\mosu_E{cell.row}.png)"
            markdown_content +="\n"
        # if image_loader.image_in(cell.coordinate):
        #     image = image_loader.get(cell.coordinate)
        #     image.save(rf"{save_dir}/mosu_{cell.coordinate}.png")  # 保存图片
        #     print(f"在单元格{cell.coordinate}中找到图片并保存")

with open(markdown_path,'w',encoding="utf-8") as f:
    f.write(markdown_content)