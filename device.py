import subprocess
import os

from cache import *


class Device:
    """Main class that represents a Device"""

    def __init__(self, api, device_id, name, description, serial_number):
        self._api = api
        self.id = device_id
        self.name = name
        self.description = description
        self.serial_number = serial_number
        self.stats = Statistics()

    def heartbeat(self):
        self._api.heartbeat(self)

    def show_cache(self):
        for reading in StatisticsReading.select():
            print('device_id={0}, cpu_temp={1}, gpu_temp={2}, at={3}'
                  .format(reading.device_id, reading.cpu_temperature, reading.gpu_temperature, reading.at))


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

    def __init__(self):
        pass

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

    def __init__(self):
        pass

    @property
    def temperature(self):
        try:
            output = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp'])
            temperature = float(output)
        except:
            return 0

        #return '{0:.2f} C'.format(temperature / 1000)
        return temperature


class Gpu:
    """GPU information"""

    def __init__(self):
        pass

    @property
    def temperature(self):
        try:
            output = subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp'])
            search = re.search(r'temp=(.*?)(?=\')', output, re.I)
            temperature = float(search.group(1))
        except:
            return 0

        return temperature
        #return '{0:.2f} C'.format(temperature)


class Memory:
    """Memory information"""

    def __init__(self):
        pass

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

    def __init__(self):
        pass

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

    def __init__(self):
        pass

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