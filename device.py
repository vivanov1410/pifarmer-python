import subprocess
import re

from cache import *


class Device:
    """Main class that represents a Device"""

    def __init__(self, api, device_id, name, description, serial_number):
        self._api = api
        self.id = device_id
        self.name = name
        self.description = description
        self.serial_number = serial_number
        self.stats = DeviceStatistics()

    def heartbeat(self):
        self._api.heartbeat(self)

    def show_cache(self):
        for reading in StatisticsReading.select():
            print('device_id={0}, at={1}, cpu_temp={2}, gpu_temp={3}'
                  .format(reading.device_id, int(reading.at), reading.cpu_temperature, reading.gpu_temperature))


class DeviceStatistics:
    def __init__(self):
        pass

    @property
    def uptime(self):
        """Returns how long the system has been up (int) (in seconds)"""
        try:
            output = subprocess.check_output(['cat', '/proc/uptime'])
            uptime = float(output.split()[0])
            return int(uptime)
        except:
            return 0

    @property
    def cpu_temperature(self):
        """Returns CPU temperature (float) in Celsius"""
        try:
            output = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp'])
            return float(output) / 1000
        except:
            return 0.0

    @property
    def gpu_temperature(self):
        """Returns GPU temperature (float) in Celsius"""
        try:
            output = subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp'])
            search = re.search(r'temp=(.*?)(?=\')', output, re.I)
            return float(search.group(1))
        except:
            return 0.0

    @property
    def memory_total(self):
        """Returns total memory (int) in bytes"""
        try:
            output = subprocess.check_output(['free', '-b'])
            total = int(output.split('\n')[1].split()[1])
            return total
        except:
            return 0

    @property
    def memory_used(self):
        """Returns used memory (int) in bytes"""
        try:
            output = subprocess.check_output(['free', '-b'])
            used = int(output.split('\n')[1].split()[2])
            return used
        except:
            return 0

    @property
    def memory_free(self):
        """Returns free memory (int) in bytes"""
        return self.memory_total - self.memory_used

    @property
    def hdd_total(self):
        """Returns total hdd space on main drive (int) in bytes"""
        try:
            output = subprocess.check_output('df')
            total = int(output.split('\n')[1].split()[1])
            return total * 1024
        except:
            return 0

    @property
    def hdd_used(self):
        """Returns used hdd space on main drive (int) in bytes"""
        try:
            output = subprocess.check_output('df')
            used = int(output.split('\n')[1].split()[2])
            return used * 1024
        except:
            return 0

    @property
    def hdd_free(self):
        """Returns free hdd space on main drive (int) in bytes"""
        return self.hdd_total - self.hdd_used
