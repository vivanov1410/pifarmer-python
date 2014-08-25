import subprocess
import os
import re
import sys

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
    """docstring for General"""
    def __init__(self):
        pass

    def uptime(self):
        try:
            output = subprocess.check_output(['uptime'])
            search = re.search(r'up\s(.*?)(?=\,)', output, re.I)
            uptime = search.group(1)
            return uptime
        except:
            print(sys.exc_info()[0])
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
    pass

  def speed(self):
    pass


class GPU:
  """docstring for GPU"""
  def __init__(self):
    pass

  def temperature(self):
    pass

  def speed(self):
    pass


class Memory:
  """docstring for Memory"""
  def __init__(self):
    pass

  def free(self):
    pass

  def total(self):
    pass

  def used(self):
    pass


class Network:
  """docstring for Network"""
  def __init__(self):
    pass

  def ip(self):
    pass

  def connections(self):
    pass
