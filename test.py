import pifarmer

device = pifarmer.connect_device('54154c97711f5f79860fb064')
device.heartbeat()

# print('general.uptime: {}'.format(device.general.uptime))
# print('general.processes: {}'.format(device.general.processes))
# print()
# print('cpu.temperature: {}'.format(device.cpu.temperature))
# print('cpu.speed: {}'.format(device.cpu.speed))
# print()
# print('gpu.temperature: {}'.format(device.gpu.temperature))
# print()
# print('memory.total: {}'.format(device.memory.total))
# print('memory.free: {}'.format(device.memory.free))
# print('memory.used: {}'.format(device.memory.used))
# print()
# print('hdd.total: {}'.format(device.hdd.total))
# print('hdd.free: {}'.format(device.hdd.free))
# print('hdd.used: {}'.format(device.hdd.used))
# print()
# print('network.ip: {}'.format(device.network.ip))
# print('network.connections: {}'.format(device.network.connections))
