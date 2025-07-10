from gen import ignore_route
from flask import Flask, request
from config_reader import read_model_config
from cache_handler import init_db, save_to_cache, get_from_cache
from controller.building_controller import BuildingController
from controller.quest_controller import QuestController
from controller.worker_controller import WorkerController
from controller.army_controller import ArmyController
import json 
from flask import send_from_directory
from database.MysqlConnector import MysqlConnector
from database.manager.SoldierManager import SoldierManager
from database.mysql_conf import LOCAL_CONF
import pandas as pd
import io

app = Flask(__name__)
MysqlConnector()

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
    return send_from_directory('static', 'html/list_page.html')


@app.route('/heros')
def heros_page():
    return send_from_directory('static', 'html/heros_page.html')

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


@app.route("/quest/chapter")
def getAllChapter():
    qc = QuestController()
    data = qc.getChapterCSV()
    df = pd.DataFrame(data)
    output = io.StringIO()
    df.to_csv(output, index=True)
    output.seek(0)
    return output, 200, {'Content-Type': 'application/csv','Content-Disposition': 'attachment; filename=data.csv'}

if __name__ == '__main__':
    init_db()
    app.run(debug=True)