from flask import Flask, request
from config_reader import read_model_config
from cache_handler import init_db, save_to_cache, get_from_cache
from controller.building_controller import BuildingController
from controller.worker_controller import WorkerController
from controller.army_controller import ArmyController
import json 
from flask import send_from_directory
from database.MysqlConnector import MysqlConnector
from database.manager.SoldierManager import SoldierManager

app = Flask(__name__)
MysqlConnector()

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


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


@app.route('/army/all')
def all_army():
    ac = ArmyController()
    return json.dumps(ac.getAll(),ensure_ascii=False,indent=4), 200, {'Content-Type': 'application/json'}

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
    return send_from_directory('templates', 'list_page.html')


@app.route('/heros')
def heros_page():
    return send_from_directory('templates', 'heros_page.html')

@app.route('/buildings')
def buildings_page():
    return send_from_directory('static/html', 'buildings_page.html')


@app.route("/add_wounded_soldiers")
def add_wounded_soldiers():
    return SoldierManager().add_wounded_soldiers()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)