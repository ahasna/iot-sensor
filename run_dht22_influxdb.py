import os
import time
from datetime import datetime

import adafruit_dht
import board
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '.env')
load_dotenv(dotenv_path)

from utils import InfluxDBTools, color_it
from utils import control_plug

dhtDevice = adafruit_dht.DHT22(board.D18)

influxdb_tools = InfluxDBTools(
    host=os.environ.get('INFLUXDB__DB_HOST', 'localhost'),
    port=os.environ.get('INFLUXDB__DB_PORT', 8086),
    db_name=os.environ.get('INFLUXDB__DB_NAME', 'test_db')
)
while True:
    data_points_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    try:
        # Print the values to the serial port
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    if temperature > 25:
        plug_state = "off"
    else:
        plug_state = "on"
    control_plug(plug_state)
    json_body = [
        {
            "measurement": os.environ.get('INFLUXDB__MEASUREMENT_NAME', 'test_measurement'),
            "tags": {"sensorId": "DHT22"},
            "time": data_points_time,
            "fields": {"temperature": temperature},
        },
        {
            "measurement": os.environ.get('INFLUXDB__MEASUREMENT_NAME', 'test_measurement'),
            "tags": {"sensorId": "DHT22"},
            "time": data_points_time,
            "fields": {"humidity": humidity},
        },
        {
            "measurement": os.environ.get('INFLUXDB__MEASUREMENT_NAME', 'test_measurement'),
            "tags": {"smartPlugId": "HS100"},
            "time": data_points_time,
            "fields": {"plugState": plug_state},
        },
    ]
    influxdb_tools.write_points(json_body)

    # colored CLI output
    info = "Temperature: {}  Humidity: {}".format(color_it(str(
        temperature) + " C", "red"), color_it(str(humidity) + " %", "red"))

    print(info, end='\r')

    time.sleep(2.0)
