import json
import logging
import os
import sys
import threading
import traceback
from uuid import uuid4
import time

from awscrt import io, mqtt
from awsiot import mqtt_connection_builder

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m-%d-%Y %H:%M:%S %Z')

received_all_event = threading.Event()
client_id = str(uuid4())
endpoint = "a2rrngjgcgkt17-ats.iot.eu-central-1.amazonaws.com"
topic = "iot_lite/2022/temp_humidity"


def on_connection_interrupted(connection, error, **kwargs):
    logging.info("Connection interrupted. error: {}".format(error))


def on_connection_resumed(connection, return_code, session_present, **kwargs):
    logging.info("Connection resumed. return_code: {} session_present: {}".format(
        return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        logging.info(
            "Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    logging.info("Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit(
                "Server rejected resubscribe to topic: {}".format(topic))

def print_full_exception():
    exception_type, exception_value, exception_traceback = sys.exc_info()
    traceback_string = traceback.format_exception(
        exception_type, exception_value, exception_traceback)
    err_msg = {
        "errorType": exception_type.__name__,
        "errorMessage": str(exception_value),
        "stackTrace": traceback_string
    }
    print(json.dumps(err_msg))
    return err_msg

event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=endpoint,
    port=443,
    cert_filepath="/home/pi/certs/device.pem.crt",
    pri_key_filepath="/home/pi/certs/private.pem.key",
    client_bootstrap=client_bootstrap,
    ca_filepath="/home/pi/certs/Amazon-root-CA-1.pem",
    on_connection_interrupted=on_connection_interrupted,
    on_connection_resumed=on_connection_resumed,
    client_id=client_id,
    clean_session=False,
    keep_alive_secs=30)

logging.info("Connecting to {} with client ID '{}'...".format(
    endpoint, client_id))

connect_future = mqtt_connection.connect()

# Future.result() waits until a result is available
connect_future.result()
logging.info("Connected!")

message = {
    "temp": 22.0,
    "humidity": 55.0
}

logging.info("Publishing message to topic '{}': {}".format(topic, message))

while True:
    try:
        mqtt_connection.publish(
            topic=topic,
            payload=json.dumps(message),
            qos=mqtt.QoS.AT_LEAST_ONCE)
    except Exception as e:
        print_full_exception()
    time.sleep(5)

