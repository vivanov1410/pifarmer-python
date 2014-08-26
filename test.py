import pifarm_device

device = pifarm_device.init()

print('general.uptime: {}'.format(device.general.uptime()))
print('general.processes: {}'.format(device.general.processes()))
print()
print('cpu.temperature: {}'.format(device.cpu.temperature()))
print('cpu.speed: {}'.format(device.cpu.speed()))
print()
print('gpu.temperature: {}'.format(device.gpu.temperature()))
print()
print('network.ip: {}'.format(device.network.ip()))
print('network.connections: {}'.format(device.network.connections()))
