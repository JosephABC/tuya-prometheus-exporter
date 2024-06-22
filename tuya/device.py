
import tuyapower
from prometheus_client import Gauge

from typing import List, Dict
import logging

# Configure the logging system
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# Define Metrics
ON = Gauge('tuya_on', 'On Status for tuya device', ['device'])
POWER = Gauge('tuya_power', 'Power consumption (W) for tuya device', ['device'])
CURRENT = Gauge('tuya_current', 'Current(mA) for tuya device', ['device'])
VOLTAGE = Gauge('tuya_voltage', 'Voltage(V) for tuya device', ['device'])


class Device:
    def __init__(self, name: str, id: str, ip: str, key: str, version: str = '3.5') -> None:
        self.name = name
        self.id = id
        self.ip = ip
        self.key = key
        self.version = version

    def query_metrics(self):
        (on, w, mA, V, err) = tuyapower.deviceInfo(
                                    self.id,
                                    self.ip,
                                    self.key,
                                    self.version
                                )
        if err != "OK":
            logger.error(f'error querying device {self.name} | {err}')
            return
        
        ON.labels(device=self.name).set(on)
        POWER.labels(device=self.name).set(w)
        CURRENT.labels(device=self.name).set(mA)
        VOLTAGE.labels(device=self.name).set(V)

class Devices:
    def __init__(self, devices_info: List[Dict[str, str]]):
        self.devices_info = devices_info
        self.devices = []

        for device_info in self.devices_info:
            self.devices.append(Device(**device_info))
            logger.info(f'device registered: {device_info.get("name")}')

    def query_all(self):
        for device in self.devices:
            device.query_metrics()
        logger.debug('query success')
    
    
    