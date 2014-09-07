import subprocess
import os
import re
import json
import socket

import requests


def get_serial():
    serial = '0000000000000000'
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                serial = line[10:26]
        f.close()
    except:
        print('Error. Could not detect serial number.')
        raise

    return serial


def online():
    server = 'www.google.com'
    try:
        host = socket.gethostbyname(server)
        socket.create_connection((host, 80), 2)
        return False
    except:
        pass
    return False


def connect_device(device_id, environment='development'):
    api = OnlineApi(environment) if online() else OfflineApi(environment)
    device = api.connect(device_id, get_serial())
    return Device(device['id'], device['name'], device['description'], device['serial_number'])


class Device:
    """Main class that represents a Device"""

    def __init__(self, device_id, name, description, serial_number):
        self.id = device_id
        self.name = name
        self.description = description
        self.serial_number = serial_number
        self.stats = Statistics()


class BaseApi:
    def __init__(self, environment='development'):
        self.base_url = 'http://localhost:54627/v1' if environment == 'development' else 'http://pifarm.apphb.com/v1'
        self.sessionToken = None


class OnlineApi(BaseApi):
    def connect(self, device_id, serial_number):
        url = '{0}/auth/login/device'.format(self.base_url)
        headers = {'content-type': 'application/json'}
        payload = {'deviceId': device_id, 'serialNumber': serial_number}

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == requests.codes.ok:
            data = response.json()
            self.sessionToken = data['sessionToken']
            deviceModel = {'id': data['id'], 'name': data['name'], 'description': data['description'], 'serial_number': data['serialNumber']}
            return deviceModel
        else:
            response.raise_for_status()


class OfflineApi(BaseApi):
    def connect(self, device_id, serial_number):
        deviceModel = {'id': device_id, 'name': 'n/a', 'description': 'n/a', 'serial_number': serial_number}
        return deviceModel


class Statistics:

    def __init__(self):
        self.general = General()
        self.cpu = Cpu()
        self.gpu = Gpu()
        self.memory = Memory()
        self.hdd = Hdd()
        self.network = Network()


class General:
    """General device information"""

    @property
    def uptime(self):
        try:
            output = subprocess.check_output(['uptime'])
            search = re.search(r'up\s(.*?)(?=\,)', output, re.I)
            uptime = search.group(1)
            return uptime
        except:
            return 'n/a'

    @property
    def processes(self):
        try:
            output = subprocess.check_output(['ps', '-e'])
            processes = len(output.split('\n'))
            return processes
        except:
            return 'n/a'


class Cpu:
    """CPU information"""

    @property
    def temperature(self):
        output = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp'])
        temperature = float(output)
        return '{0:.2f} C'.format(temperature / 1000)

    @property
    def speed(self):
        f = os.popen('sudo cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq')
        speed = float(f.read())
        return '{0} MHz'.format(speed / 1000)


class Gpu:
    """GPU information"""

    @property
    def temperature(self):
        output = subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp'])
        search = re.search(r'temp=(.*?)(?=\')', output, re.I)
        temperature = float(search.group(1))
        return '{0:.2f} C'.format(temperature)


class Memory:
    """Memory information"""

    @property
    def total(self):
        try:
            output = subprocess.check_output(['free', '-m'])
            total = output.split('\n')[1].split()[1]
            return '{} MB'.format(int(total))
        except:
            return 'n/a'

    @property
    def used(self):
        output = subprocess.check_output(['free', '-m'])
        used = output.split('\n')[1].split()[2]
        return '{} MB'.format(int(used))

    @property
    def free(self):
        try:
            output = subprocess.check_output(['free', '-m'])
            free = output.split('\n')[1].split()[3]
            return '{} MB'.format(int(free))
        except:
            return 'n/a'


class Hdd:
    """HDD information"""

    @property
    def total(self):
        try:
            output = subprocess.check_output(['df', '-h'])
            total = output.split('\n')[1].split()[1]
            return total
        except:
            return 'n/a'

    @property
    def used(self):
        output = subprocess.check_output(['df', '-h'])
        used = output.split('\n')[1].split()[2]
        return used

    @property
    def free(self):
        try:
            output = subprocess.check_output(['df', '-h'])
            free = output.split('\n')[1].split()[3]
            return free
        except:
            return 'n/a'


class Network:
    """docstring for Network"""

    @property
    def ip(self):
        try:
            output = subprocess.check_output(['ip', 'route', 'list']).split()
            index = output.index('src') + 1
            ip = output[index]
            return ip
        except:
            return 'n/a'

    @property
    def connections(self):
        try:
            output = subprocess.check_output(['netstat', '-tun'])
            return len([x for x in output.split() if x == 'ESTABLISHED'])
        except:
            return 'n/a'