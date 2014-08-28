import subprocess
import os
import re


def init():
    return Device()


class Device:
    """Main class that represents a Device"""

    def __init__(self):
        self.general = General()
        self.cpu = CPU()
        self.gpu = GPU()
        self.memory = Memory()
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
        output = subprocess.check_output(['free', '-m'])
        used = output.split('\n')[1].split()[2]
        return used

    @property
    def free(self):
        try:
            output = subprocess.check_output(['free', '-m'])
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