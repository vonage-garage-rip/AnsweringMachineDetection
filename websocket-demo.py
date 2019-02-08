#!/usr/bin/env python

from __future__ import absolute_import, print_function

import io
import logging
import os
import sys
import time
from logging import debug, info
import uuid
import cgi
import nexmo

import requests
import tornado.ioloop
import tornado.websocket
import tornado.httpserver
import tornado.template
import tornado.web
import webrtcvad
from tornado.web import url
import json

from base64 import b64decode

#Only used for record function
import datetime
import wave

import numpy as np
from scipy.io import wavfile
import librosa
import pickle
from google.cloud import storage

from dotenv import load_dotenv
from sklearn.naive_bayes import GaussianNB

load_dotenv()

os.environ['KMP_DUPLICATE_LIB_OK']='True'

logging.captureWarnings(True)


# Constants:
MS_PER_FRAME = 15  # Duration of a frame in ms
MY_LVN = os.getenv("MY_LVN")
APP_ID = os.getenv("APP_ID")
PROJECT_ID = os.getenv("PROJECT_ID")
CLOUD_STORAGE_BUCKET = os.getenv("CLOUD_STORAGE_BUCKET")

def _get_private_key():
    try:
        return os.environ['PRIVATE_KEY']
    except:
        with open('private.key', 'r') as f:
            private_key = f.read()

    return private_key

PRIVATE_KEY = _get_private_key()
if PROJECT_ID and CLOUD_STORAGE_BUCKET:
    storage_client = storage.Client(PROJECT_ID)
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)

# Global variables
conns = {}
clients = []
conversation_uuids = dict()
uuids = []

loaded_model = pickle.load(open("models/GaussianNB-20190130T1233.pkl", "rb"))
print(loaded_model)
client = nexmo.Client(application_id=APP_ID, private_key=PRIVATE_KEY)
print(client)
class BufferedPipe(object):
    def __init__(self, max_frames, sink):
        """
        Create a buffer which will call the provided `sink` when full.

        It will call `sink` with the number of frames and the accumulated bytes when it reaches
        `max_buffer_size` frames.
        """
        self.sink = sink
        self.max_frames = max_frames

        self.count = 0
        self.payload = b''

    def append(self, data, id):
        """ Add another data to the buffer. `data` should be a `bytes` object. """

        self.count += 1
        self.payload += data

        if self.count == self.max_frames:
            self.process(id)

    def process(self, id):
        """ Process and clear the buffer. """
        self.sink(self.count, self.payload, id)
        self.count = 0
        self.payload = b''

class AudioProcessor(object):
    def __init__(self, path, rate, clip_min, uuid):
        self.rate = rate
        self.bytes_per_frame = rate/25
        self._path = path
        self.clip_min_frames = clip_min // MS_PER_FRAME
        self.uuid = uuid
    def process(self, count, payload, id):
        if count > self.clip_min_frames:  # If the buffer is less than CLIP_MIN_MS, ignore it
            fn = "{}rec-{}-{}.wav".format('', id, datetime.datetime.now().strftime("%Y%m%dT%H%M%S"))
            output = wave.open(fn, 'wb')
            output.setparams((1, 2, self.rate, 0, 'NONE', 'not compressed'))
            output.writeframes(payload)
            output.close()
            debug('File written {}'.format(fn))
            self.process_file(fn)
            info('Processing {} frames for {}'.format(str(count), id))
            self.removeFile(fn)
        else:
            info('Discarding {} frames'.format(str(count)))
    def process_file(self, wav_file):
        if loaded_model != None:
            print("load file {}".format(wav_file))

            X, sample_rate = librosa.load(wav_file, res_type='kaiser_fast')
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
            X = [mfccs]
            prediction = loaded_model.predict(X)
            print("prediction",prediction)

            if prediction[0] == 0:
                beep_captured = True
                print("beep detected")
            else:
                beep_captured = False

            for client in clients:
                client.write_message({"uuids":uuids, "beep_detected":beep_captured})

        else:
            print("model not loaded")
    def removeFile(self, wav_file):
         os.remove(wav_file)

class WSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self):
        # Create a buffer which will call `process` when it is full:
        self.frame_buffer = None
        # Setup the Voice Activity Detector
        self.tick = None
        self.id = uuid.uuid4().hex
        self.vad = webrtcvad.Vad()
          # Level of sensitivity
        self.processor = None
        self.path = None
        self.rate = None #default to None
        self.silence = 20 #default of 20 frames (400ms)
        conns[self.id] = self
    def open(self, path):
        info("client connected")
        clients.append(self)
        debug(self.request.uri)
        self.path = self.request.uri
        self.tick = 0
    def on_message(self, message):
        # Check if message is Binary or Text
        if type(message) != str:
            # print(self.rate)
            if self.vad.is_speech(message, self.rate):
                debug ("SPEECH from {}".format(self.id))
                self.tick = self.silence
                self.frame_buffer.append(message, self.id)
            else:
                debug("Silence from {} TICK: {}".format(self.id, self.tick))
                self.tick -= 1
                if self.tick == 0:
                    self.frame_buffer.process(self.id)  # Force processing and clearing of the buffer
        else:
            # Here we should be extracting the meta data that was sent and attaching it to the connection object
            data = json.loads(message)
            print("on_message",data)
            if data.get('content-type'):
                m_type, m_options = cgi.parse_header(data['content-type'])
                self.rate = 16000
                # region = data.get('aws_region', 'us-east-1')
                clip_min = int(data.get('clip_min', 200))
                clip_max = int(data.get('clip_max', 10000))
                silence_time = int(data.get('silence_time', 300))
                sensitivity = int(data.get('sensitivity', 3))
                uuid = data.get('uuid')
                self.vad.set_mode(sensitivity)
                self.silence = silence_time // MS_PER_FRAME
                self.processor = AudioProcessor(self.path, self.rate, clip_min, uuid).process
                self.frame_buffer = BufferedPipe(clip_max // MS_PER_FRAME, self.processor)
                self.write_message('ok')
    def on_close(self):
        print("close")
        # Remove the connection from the list of connections
        del conns[self.id]
        clients.remove(self)
        info("client disconnected")


class PingHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write('ok')
        self.set_header("Content-Type", 'text/plain')
        self.finish()

class EventHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        # print("event:", self.request.body)

        data = json.loads(self.request.body)
        try:
            if data["status"] == "answered":
                uuid = data["uuid"]
                uuids.append(uuid)
                conversation_uuid = data["conversation_uuid"]
                conversation_uuids[conversation_uuid] = uuid
                print(conversation_uuids)
        except:
            pass


        try:
            if data["status"] == "completed":
                uuids.clear()

                ws_conversation_id = conversation_uuids[data["conversation_uuid"]]
                response = client.update_call(ws_conversation_id, action='hangup')
                conversation_uuids[data["conversation_uuid"]] = ''
                print(response)

        except Exception as e:
            print(e)
            pass


        self.content_type = 'text/plain'
        self.write('ok')
        self.finish()

class EnterPhoneNumberHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        ncco = [
              {
                "action": "talk",
                "text": "Please enter a phone number to dial"
              },
              {
                "action": "input",
                "eventUrl": [self.request.protocol +"://" + self.request.host +"/ivr"],
                "timeOut":10,
                "maxDigits":12,
                "submitOnHash":True
              }

            ]
        self.write(json.dumps(ncco))
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.finish()


class AcceptNumberHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        data = json.loads(self.request.body)
        print(data)
        ncco = [
              {
                "action": "talk",
                "text": "Thanks. Connecting you now"
              },
            {
                "action": "record",
                "eventUrl": [self.request.protocol +"://" + self.request.host  +"/recording"],
              },
             {
             "action": "connect",
              "eventUrl": [self.request.protocol +"://" + self.request.host  + "/event"],
               "from": MY_LVN,
               "endpoint": [
                 {
                   "type": "phone",
                   "number": data["dtmf"]
                 }
               ]
             },
              {
                 "action": "connect",
                 "eventUrl": [self.request.protocol +"://" + self.request.host  +"/event"],
                 "from": MY_LVN,
                 "endpoint": [
                     {
                        "type": "websocket",
                        "uri" : "ws://"+self.request.host +"/socket",
                        "content-type": "audio/l16;rate=16000",
                        "headers": {
                            "uuid":data["uuid"]
                        }
                     }
                 ]
               }
            ]
        self.write(json.dumps(ncco))
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.finish()

class RecordHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        data = json.loads(self.request.body)

        response = client.get_recording(data["recording_url"])
        fn = "call-{}.wav".format(data["conversation_uuid"])

        if PROJECT_ID and CLOUD_STORAGE_BUCKET:
            blob = bucket.blob(fn)
            blob.upload_from_string(response, content_type="audio/wav")
            print('File uploaded.')

        self.write('ok')
        self.set_header("Content-Type", 'text/plain')
        self.finish()

def main():
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)7s %(message)s",
        )
        application = tornado.web.Application([
			url(r"/ping", PingHandler),
            (r"/event", EventHandler),
            (r"/ncco", EnterPhoneNumberHandler),
            (r"/recording", RecordHandler),
            (r"/ivr", AcceptNumberHandler),
            url(r"/(.*)", WSHandler),
        ])
        http_server = tornado.httpserver.HTTPServer(application)
        port = int(os.getenv('PORT', 8000))
        http_server.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass  # Suppress the stack-trace on quit


if __name__ == "__main__":
    main()
