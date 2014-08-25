import pifarm_device

device = pifarm_device.init()

print(device.general.uptime())
