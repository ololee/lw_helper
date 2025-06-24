from flask import Flask, request
from config_reader import read_model_config
from cache_handler import init_db, save_to_cache, get_from_cache
from controller.hero_controller import HeroController
import json 
from flask import send_from_directory

app = Flask(__name__)

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


@app.route('/workers')
def list_page():
    workers = HeroController().getALl()
    return json.dumps(workers), 200, {'Content-Type': 'application/json'}

@app.route('/filter')
def filter():
    workerId = request.args.get('workerId')
    workers = HeroController().getWorkerCfgById(workerId)
    return json.dumps([workers]), 200, {'Content-Type': 'application/json'}

@app.route('/list_page.html')
def serve_list_page():
    return send_from_directory('templates', 'list_page.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)