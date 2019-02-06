#!/usr/bin/python
import websocket
import time
import os
import nexmo
import json
from dotenv import load_dotenv
load_dotenv()

HOSTNAME =  os.getenv("HOSTNAME")#Change to the hostname of your server
NEXMO_NUMBER = os.getenv("NEXMO_NUMBER")
NEXMO_APP_ID = "3072bbc8-c237-4d05-ab6e-2faec95c72e3"
CONF_NAME = os.getenv("CONF_NAME")

client = nexmo.Client(application_id=NEXMO_APP_ID, private_key=NEXMO_APP_ID+".key")
print(client)


def on_message(ws, message):
    data = json.loads(message)
    print(data)
    if data["beep_detected"] == True:
        for id in data["uuids"]:
            print("id",id)
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
    ws = websocket.WebSocketApp("ws://careangel-amd-detector.herokuapp.com/socket",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()
