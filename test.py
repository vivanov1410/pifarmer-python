import pifarm_device

device = pifarm_device.init()

print('general.uptime: {}'.format(device.general.uptime()))
print('general.processes: {}'.format(device.general.processes()))
