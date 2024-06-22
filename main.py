from prometheus_client import start_http_server
import yaml

import random
import time
import logging

from tuya.device import Devices

# Configure the logging system
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# Configuration
def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

# Create metrics
# VOLTAGE = Gauge('tuya_smartplug_voltage', 'Voltage of Tuya smart plug')

if __name__ == '__main__':
    # Read Config
    logger.info("Read Config")

    config = load_config('config.yaml')
    logger.setLevel(config['logging']['level'])

    logger.debug(config)


    # Create Devices
    devices = Devices(config['devices'])

    # Serve from webserver
    logger.info("Starting Webserver")
    start_http_server(9090)
    while True:
        devices.query_all()

        time.sleep(config.get('scrapeInterval', 10))
