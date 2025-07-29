from pandas.core._numba import executor
from decompile import decompile
from gen import ignore_route,routes
from flask import Flask, render_template, request, jsonify
from config_reader import read_model_config
from cache_handler import init_db, save_to_cache, get_from_cache
from controller.building_controller import BuildingController
from controller.quest_controller import QuestController
from controller.worker_controller import WorkerController
from controller.army_controller import ArmyController
from controller.hero_controller import HeroController
from controller.skill_controller import SkillController
from controller.hero_skill_controller import HeroSkillController
from decompile.decompile import Decompiler
from flask_socketio import SocketIO
import os
from concurrent.futures import ThreadPoolExecutor
from decompile.cmd.CMD_utils import CMD_utils

import json 
from flask import send_from_directory
from database.MysqlConnector import MysqlConnector
from database.manager.SoldierManager import SoldierManager
from database.mysql_conf import LOCAL_CONF
import pandas as pd
import io

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
socketio = SocketIO(app,cors_allowed_origins="*")
MysqlConnector()
executor = ThreadPoolExecutor(max_workers=4)


def get_file_info(root_dir,path):
    relative_path = os.path.relpath(path, root_dir).replace("\\", "/")
    """获取文件或目录的信息"""
    info = {
        "root": root_dir.replace("\\", "/"),
        'name': os.path.basename(path),
        'path': relative_path,
        'is_dir': os.path.isdir(path),
        'size': os.path.getsize(path) if not os.path.isdir(path) else 0,
        'mtime': os.path.getmtime(path)
    }
    return info

@ignore_route
@app.route('/file_select/list', methods=['GET'])
def list_files():
    root_dir = Decompiler().getExportDir()
    """列出指定目录下的文件和文件夹"""
    dir_path = request.args.get('path', '')
    abs_path = os.path.join(root_dir, dir_path)
    
    # 安全检查：确保请求的路径在允许的根目录内
    if not os.path.abspath(abs_path).startswith(root_dir):
        return jsonify({'error': 'Access denied'}), 403
    
    if not os.path.exists(abs_path) or not os.path.isdir(abs_path):
        return jsonify({'error': 'Directory not found'}), 404
    
    try:
        items = []
        for item in os.listdir(abs_path):
            item_path = os.path.join(abs_path, item)
            items.append(get_file_info(root_dir,item_path))

        # if dir_path == None or dir_path == '':
        #     for item in os.list
        
        # 按名称排序，文件夹优先
        items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ignore_route
@app.route("/save_choosed_file",methods=['POST'])
def save_choosed_file():
    data = request.get_json()
    file_path = data['file_path']
    decompiler = Decompiler()
    result = decompiler.save_file(file_path)
    if result["error"] == None or result["error"] == "":
        socketio.emit('save_choosed_file_result', result)
    return json.dumps(result), 200, {'Content-Type': 'application/json'}

@ignore_route
@app.route('/get_file')
def get_file():
    return render_template('file_browser.html')

@ignore_route
@app.route("/app_home")
def getHomePageData():
    return routes

@ignore_route
@app.route('/')
def index():
     return send_from_directory('static', "html/index.html")

@ignore_route
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@ignore_route
@app.route('/worker/<id>')
def getHeroCfgById(id):
    try:
        worker_cfgs = read_model_config('./static/config/csv/lw_worker.csv')
        for cfg in worker_cfgs:
            if str(cfg['id']) == str(id):
                return json.dumps(cfg), 200, {'Content-Type': 'application/json'}
        return json.dumps({'error': 'Hero not found'}), 404, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({'error': str(e)}), 500, {'Content-Type': 'application/json'}


@app.route('/workers/all')
def list_page():
    wc = WorkerController()
    workers = wc.getALl()
    return json.dumps(workers), 200, {'Content-Type': 'application/json'}


@app.route('/skill/all')
def all_skills():
    sc = SkillController()
    skills = sc.getALl()
    return json.dumps(skills,ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

@app.route('/hero_skill/all')
def all_hero_skills():
    hsc = HeroSkillController()
    skills = hsc.getALl()
    return json.dumps(skills,ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

@app.route('/buildings/all')
def all_buildings():
    bc = BuildingController()
    return json.dumps(bc.getAll(),ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

@ignore_route
@app.route("/building/<id>")
def get_building_details(id):
    bc = BuildingController()
    return json.dumps(bc.getById(id),ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}


@app.route('/army/all')
def all_army():
    ac = ArmyController()
    return json.dumps(ac.getAll(),ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

@ignore_route
@app.route('/filter')
def filter():
    workerId = request.args.get('workerId')
    quality = request.args.get('quality')
    job = request.args.get('job')
    print(workerId,quality,job)
    workers = WorkerController().filter(workerId,int(quality),job)
    return json.dumps(workers), 200, {'Content-Type': 'application/json'}

@app.route('/workers')
def serve_list_page():
    return send_from_directory('static', 'html/worker_page.html')

@app.route('/heros/all')
def all_heros():
    hc = HeroController()
    return json.dumps(hc.getAll(),ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

@app.route('/heros')
def heros_page():
    return send_from_directory('static', 'html/hero_page.html')

@app.route('/hero_skills')
def hero_skills_page():
    return send_from_directory('static', 'html/hero_skill_page.html')

@ignore_route
@app.route('/hero_filter')
def hero_filter():
    heroId = request.args.get('heroId')
    quality = request.args.get('quality')
    isHuman = request.args.get('isHuman')
    onlyList = request.args.get('onlyList')
    heros = HeroController().filter(heroId,int(quality),isHuman,onlyList)
    return json.dumps(heros), 200, {'Content-Type': 'application/json'}
@app.route('/buildings')
def buildings_page():
    return send_from_directory('static/html', 'buildings_page.html')


@app.route("/add_wounded_soldiers")
def add_wounded_soldiers():
    return SoldierManager().add_wounded_soldiers()

@app.route("/reset_db")
def reset_db():
    connector = MysqlConnector()
    connector.connect()
    local_sql_path = LOCAL_CONF["local_sql"]
    with open(local_sql_path, "r",encoding="utf-8") as f:
        sql = f.read()
        connector.execute(sql)
    connector.close()
    return  json.dumps({},ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

@app.route("/quest/all")
def get_all_quest():
    qc = QuestController()
    return  json.dumps(qc.getAll(),ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}


@app.route("/quest")
def quest():
    return send_from_directory('static/html', 'quest_page.html')

@app.route("/decode")
def decode():
    return send_from_directory('static/html', 'decode_unicode_strs.html')

@app.route("/decompile")
def compile_page():
    return send_from_directory('static/html', 'decompile_page.html')

@ignore_route
@app.route("/decompile/fetchFiles",methods=["POST"])
def get_ls_scripts():
    decompiler = Decompiler()
    data = request.get_json()
    task_id = data["taskId"]
    result = decompiler.pull_Lw_scripts(task_id)
    return  json.dumps(result,ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

def progress_callback(idx,name,count):
    global socketio
    if idx < count:
        if idx % 100 == 0:
            socketio.emit("progress_update", {
                "taskId":2,
                "idx": idx,
                "name": name,
                "count": count
            })
            socketio.sleep(0)
    else:
        socketio.emit("progress_update", {
            "taskId":2,
            "idx": idx,
            "name": name,
            "count": count
        })
        socketio.sleep(0)


def start_unzipFiles():
    decompiler = Decompiler()
    decompiler.unzipFiles(progress_callback)

@ignore_route
@app.route("/decompile/unzipFiles",methods=["POST"])
def unzipFiles():
    data = request.get_json()
    task_id = data["taskId"]
    socketio.start_background_task(start_unzipFiles)
    return  json.dumps({
        "task_id": task_id,
        "status": "task_started"
    },ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

@ignore_route
@app.route("/decompile/getExportDir")
def getExportDir():
    decompiler = Decompiler()
    return json.dumps({
       "path": decompiler.getExportDir()
    },ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

@ignore_route
@app.route("/decompile/decompile",methods=["POST"])
def decompile():
    decompiler = Decompiler()
    return json.dumps(decompiler.decompile(),ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}


@ignore_route
@app.route("/decompile/getCode",methods=["POST"])
def getCode():
    data = request.get_json()
    task_id = data["taskId"]
    lua_path = None
    if lua_path in data:
        lua_path = data["lua_path"]
    decompiler = Decompiler()
    code_data = decompiler.getCode(lua_path)
    return json.dumps(code_data,ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}


@ignore_route
@app.route("/decompile/code/<token>")
def open_in_webpage(token):
    decompiler = Decompiler()
    code_data = decompiler.getCodeByToken(token)
    return render_template("code_page.html",data=code_data)

@ignore_route
@app.route('/open-in-vscode', methods=['POST'])
def open_in_vscode():
    data = request.get_json()
    path = data.get('path')
    if path and os.path.exists(path):
        # 使用subprocess打开VSCode
        CMD_utils.execute_cmd(f"code {path}")
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': '文件不存在'})

@ignore_route
@app.route('/save-code', methods=['POST'])
def save_code():
    data = request.get_json()
    path = data.get('path')
    content = data.get('content')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@ignore_route
@app.route('/load-code')
def load_code():
    path = request.args.get('path')
    if path and os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

@ignore_route
@app.route("/decompile/lua2luac",methods=["POST"])
def lua2luac():
    decompiler = Decompiler()
    result = decompiler.generate_luac()
    return json.dumps(result,ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

@ignore_route
@app.route("/decompile/replace_origin_file",methods=["POST"])
def replace_origin_file():
    decompiler = Decompiler()
    result = decompiler.replace_origin_file()
    return json.dumps(result,ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

@app.route("/quest/chapter")
def getAllChapter():
    qc = QuestController()
    data = qc.getChapterCSV()
    df = pd.DataFrame(data)
    output = io.StringIO()
    df.to_csv(output, index=True)
    output.seek(0)
    return output, 200, {'Content-Type': 'application/csv','Content-Disposition': 'attachment; filename=data.csv'}


@ignore_route
@app.route("/decompile/packFiles",methods=["POST"])
def packFiles():
    decompiler = Decompiler()
    result = decompiler.packFiles()
    return json.dumps(result,ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}


@ignore_route
@app.route("/decompile/uploadResult",methods=["POST"])
def uploadResult():
    decompiler = Decompiler()
    result = decompiler.uploadResult()
    return json.dumps(result,ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    init_db()
    socketio.run(app,debug=True)