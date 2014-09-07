import platform
import subprocess

from system_detector import SystemDetector

class SerialNumberDetector:
    def __init__(self):
        self.system_detector = SystemDetector()

    @property
    def serial_number(self):
        system = self.system_detector
        serial = None
        if system.linux:
            serial = self._linux_serial_number()
        elif system.windows:
            serial = self._windows_serial_number()
        elif system.macos:
            serial = self._macos_serial_number()

        #serial = self._get_linux_serial() if system == 'Linux' else self._get_windows_serial()
        return serial

    def _linux_serial_number(self):
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

    def _windows_serial_number(self):
        try:
            output = subprocess.check_output('wmic bios get serialnumber', shell=True)
            lines = output.decode('utf-8').split('\n')
            serial = lines[1]
        except:
            print('Error. Could not detect serial number.')
            raise

        return serial

    def _macos_serial_number(self):
        try:
            output = subprocess.check_output("system_profiler SPHardwareDataType | awk '/Serial/ {print $4}'", shell=True)
            serial = output.decode('utf-8')
        except:
            print('Error. Could not detect serial number.')
            raise

        return serial


