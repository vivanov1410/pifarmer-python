import json
import time
from datetime import datetime

import requests

from cache import *


class BaseApi:
    def __init__(self, environment='development'):
        self.base_url = 'http://pifarm-api.herokuapp.com/v1' if environment == 'development' else 'http://pifarm.apphb.com/v1'
        self.sessionToken = None
        self._cache = None


class OnlineApi(BaseApi):
    def connect(self, device_id, serial_number):
        url = '{0}/auth/login-device'.format(self.base_url)
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

    def heartbeat(self, device):
        at = datetime.utcnow()

        url = '{0}/devices/{1}/stats'.format(self.base_url)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.sessionToken}
        payload = {'uptime': device.uptime,
                   'temperature': {'cpu': device.cpu_temperature, 'gpu': device.gpu_temperature},
                   'memory': {'total': device.memory_total, 'used': device.memory_used},
                   'hdd': {'total': device.hdd_total, 'used': device.hdd_used},
                   at: str(datetime.utcnow())}

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == requests.codes.ok:
            return True
        else:
            response.raise_for_status()


class OfflineApi(BaseApi):
    def connect(self, device_id, serial_number):
        self._cache = Cache()
        device_model = {'id': device_id, 'name': 'n/a', 'description': 'n/a', 'serial_number': serial_number}
        return device_model

    def heartbeat(self, device):
        stats = device.stats
        reading = StatisticsReading(device_id=device.id,
                                    uptime=stats.uptime,
                                    cpu_temperature=stats.cpu_temperature,
                                    gpu_temperature=stats.gpu_temperature,
                                    memory_total=stats.memory_total,
                                    memory_used=stats.memory_used,
                                    hdd_total=stats.hdd_total,
                                    hdd_used=stats.hdd_used,
                                    at=time.time())
        reading.save()
