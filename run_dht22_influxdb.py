import time
import os
from os.path import join, dirname
from dotenv import load_dotenv

from datetime import datetime

import Adafruit_DHT
import RPi.GPIO as GPIO
from dotenv import load_dotenv

from utils import InfluxDBTools, color_it

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

led_pin = 4
sensor_pin = 14

# initialize GPIO, First we stop the warnings which is a feature in this Python GPIO library.
GPIO.setwarnings(False)
# We also set the GPIO mode to BCM which is kind of standret RaspberryPi GPIO mapping scheme.
GPIO.setmode(GPIO.BCM)
# Finally we do a cleanup() this means that we set all GPIO pins to its default state.
GPIO.cleanup()

# Setting GPIO pin no. 14 as an output.
GPIO.setup(led_pin, GPIO.OUT)
# then we set it's state to one which equivalent to "OFF"
GPIO.output(led_pin, 0)

influxdb_tools = InfluxDBTools(
    host=os.environ.get('INFLUXDB__DB_HOST', 'localhost'),
    port=os.environ.get('INFLUXDB__DB_PORT', 8086),
    db_name=os.environ.get('INFLUXDB__DB_NAME', 'test_measurement')
    )
while True:
    humidity_long, temperature_long = Adafruit_DHT.read_retry(
        Adafruit_DHT.AM2302, sensor_pin)
    data_points_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    humidity = round(humidity_long, 3)
    temperature = round(temperature_long, 3)
    json_body = [
        {
            "measurement": os.environ.get('MEASUREMENT_NAME', 'test_measurement'),
            "tags": {"sensorId": "DHT22"},
            "time": data_points_time,
            "fields": {"temperature": temperature},
        },
        {
            "measurement": os.environ.get('MEASUREMENT_NAME', 'test_measurement'),
            "tags": {"sensorId": "DHT22"},
            "time": data_points_time,
            "fields": {"humidity": humidity},
        },
    ]
    influxdb_tools.write_points(json_body)

    # colored CLI output
    info = "Temperature: {}  Humidity: {}".format(color_it(str(
        temperature) + " C", "red"), color_it(str(humidity) + " %", "red"))

    print(info, end='\r')

    time.sleep(10)
