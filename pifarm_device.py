import subprocess
import os
import re


def init():
    return Device()


class Device:
    """docstring for Device"""

    def __init__(self):
        self.general = General()
        self.cpu = CPU()
        self.gpu = GPU()
        self.memory = Memory()
        self.network = Network()


class General:
    """General device information"""

    def __init__(self):
        pass

    def uptime(self):
        try:
            output = subprocess.check_output(['uptime'])
            search = re.search(r'up\s(.*?)(?=\,)', output, re.I)
            uptime = search.group(1)
            return uptime
        except:
            return 'n/a'

    def processes(self):
        try:
            output = subprocess.check_output(['ps', '-e'])
            processes = len(output.split('\n'))
            return processes
        except:
            return 'n/a'


class CPU:
    """docstring for CPU"""

    def __init__(self):
        pass

    def temperature(self):
        output = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp'])
        temperature = float(output)
        return '{0:.2f} C'.format(temperature / 1000)

    def speed(self):
        f = os.popen('sudo cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq')
        speed = float(f.read())
        return '{0} MHz'.format(speed / 1000)


class GPU:
    """docstring for GPU"""

    def __init__(self):
        pass

    def temperature(self):
        output = subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp'])
        search = re.search(r'temp=(.*?)(?=\')', output, re.I)
        temperature = float(search.group(1))
        return '{0:.2f} C'.format(temperature)


class Memory:
    """docstring for Memory"""

    def __init__(self):
        pass

    def total(self):
        try:
            output = subprocess.check_output(['free', '-m'])
            free = output.split('\n')[1].split()[1]
            return '{} MB'.format(int(free))
        except:
            return 'n/a'

    def used(self):
        output = subprocess.check_output(['free', '-m'])
        free = output.split('\n')[1].split()[2]
        return '{} MB'.format(int(free))

    def free(self):
        try:
            output = subprocess.check_output(['free', '-m'])
            free = output.split('\n')[1].split()[3]
            return '{} MB'.format(int(free))
        except:
            return 'n/a'


class Network:
    """docstring for Network"""

    def __init__(self):
        pass

    def ip(self):
        try:
            output = subprocess.check_output(['ip', 'route', 'list']).split()
            index = output.index('src') + 1
            ip = output[index]
            return ip
        except:
            return 'n/a'

    def connections(self):
        try:
            output = subprocess.check_output(['netstat', '-tun'])
            return len([x for x in output.split() if x == 'ESTABLISHED'])
        except:
            return 'n/a'
