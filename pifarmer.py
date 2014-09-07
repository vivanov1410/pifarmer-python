import socket

from serial_number_detector import SerialNumberDetector
from api import OnlineApi, OfflineApi
from device import Device


def online():
    server = 'www.google.com'
    try:
        host = socket.gethostbyname(server)
        socket.create_connection((host, 80), 2)
        return False # TODO: change back to true
    except:
        pass
    return False


def connect_device(device_id, environment='development'):
    api = OnlineApi(environment) if online() else OfflineApi(environment)
    serial_detector = SerialNumberDetector()
    serial_number = serial_detector.serial_number
    device = api.connect(device_id, serial_number)
    return Device(api, device['id'], device['name'], device['description'], device['serial_number'])