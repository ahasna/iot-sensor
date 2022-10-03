import asyncio
import json
import logging
import os
import sys
import time

from kasa import SmartPlug

SMART_PLUG_IP = "192.168.178.79"
plug = SmartPlug(SMART_PLUG_IP)

def control_plug(state):
    try:
        if state == "on":
            asyncio.run(plug.update())
            asyncio.run(plug.turn_on())
            logging.info('turned plug on')
        elif state == "off":
            asyncio.run(plug.update())
            asyncio.run(plug.turn_off())
            logging.info('turned plug off')
    except Exception as e:
        logging.error(e)