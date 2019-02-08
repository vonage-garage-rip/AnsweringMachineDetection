#!/usr/bin/python
import websocket
import os
import nexmo
import json
import time
from dotenv import load_dotenv
load_dotenv()

def _get_private_key():
    try:
        return os.environ['PRIVATE_KEY']
    except:
        with open('private.key', 'r') as f:
            private_key = f.read()

    return private_key

HOSTNAME =  os.getenv("HOSTNAME")
APP_ID = os.getenv("APP_ID")
PRIVATE_KEY = _get_private_key()

client = nexmo.Client(application_id=APP_ID, private_key=PRIVATE_KEY)


def on_message(ws, message):
    data = json.loads(message)
    print(data)
    if data["beep_detected"] == True:
        for id in data["uuids"]:
            response = client.send_speech(id, text='Answering Machine Detected')
            print(response)

        time.sleep(4)
        for id in data["uuids"]:
            try:
                client.update_call(id, action='hangup')
            except:
                pass

        # response = client.send_speech(data["uuid"], text='Answering Machine Detected')

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### opened ###")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://"+HOSTNAME+"/socket",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()
