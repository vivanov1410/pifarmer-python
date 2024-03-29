import socket

from serial_number_detector import SerialNumberDetector
from api import OnlineApi, OfflineApi
from device import Device


def online():
    server = 'www.google.com'
    try:
        host = socket.gethostbyname(server)
        socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


def connect_device(device_id, environment='development'):
    serial_number = SerialNumberDetector().serial_number
    api = OnlineApi(environment) if online() else OfflineApi(environment)
    device = api.connect(device_id, serial_number)
    return Device(api, device['id'], device['name'], device['description'], device['serial_number'])
