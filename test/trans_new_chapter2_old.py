from config_reader import read_model_config
import json

newChapter = read_model_config("../static/config/json/new_chapter.json")

subtaskstr = newChapter["chapterTask"]["subTasks"]
subtasks = subtaskstr.split("|")


rep_dict = dict()
out_str = json.dumps(newChapter,indent=4)
for i in range(0,len(subtasks)):
    rep_dict[subtasks[i]] = f"10001{(i+1):02d}"
    out_str = out_str.replace(subtasks[i],rep_dict[subtasks[i]])

print(out_str)