import json
from cache import *

import requests


class BaseApi:
    def __init__(self, environment='development'):
        self.base_url = 'http://localhost:54627/v1' if environment == 'development' else 'http://pifarm.apphb.com/v1'
        self.sessionToken = None
        self._cache = None


class OnlineApi(BaseApi):
    def connect(self, device_id, serial_number):
        url = '{0}/auth/login/device'.format(self.base_url)
        headers = {'content-type': 'application/json'}
        payload = {'deviceId': device_id, 'serialNumber': serial_number}

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == requests.codes.ok:
            data = response.json()
            self.sessionToken = data['sessionToken']
            device_model = {'id': data['id'], 'name': data['name'], 'description': data['description'], 'serial_number': data['serialNumber']}
            return device_model
        else:
            response.raise_for_status()


class OfflineApi(BaseApi):
    def connect(self, device_id, serial_number):
        self._cache = Cache(device.id)
        device_model = {'id': device_id, 'name': 'n/a', 'description': 'n/a', 'serial_number': serial_number}
        return device_model

    def heartbeat(self, device):
        db = SqliteDatabase(device.id + '.db')