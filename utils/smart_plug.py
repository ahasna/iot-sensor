import asyncio
import logging
import os

from kasa import SmartPlug

SMART_PLUG_IP = os.environ.get('SMART_PLUG_IP')
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
        return True
    except Exception as e:
        logging.error(e)
        return False