import platform
import subprocess


class SerialDetector:
    def __init__(self):
        pass

    @property
    def serial_number(self):
        system = platform.system()
        serial = self._get_linux_serial() if system == 'Linux' else self._get_windows_serial()
        return serial

    def _get_linux_serial(self):
        serial = None
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

    def _get_windows_serial(self):
        try:
            output = subprocess.check_output('wmic bios get serialnumber', shell=True)
            lines = output.decode('utf-8').split('\n')
            serial = lines[1]
        except:
            print('Error. Could not detect serial number.')
            raise

        return serial


