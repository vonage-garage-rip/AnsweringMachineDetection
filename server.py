import tornado.ioloop
import tornado.web
import json
import os
from dotenv import load_dotenv
load_dotenv()

HOSTNAME =  'careangel-amd-detector.herokuapp.com'#os.getenv("HOSTNAME")#Change to the hostname of your server
NEXMO_NUMBER = os.getenv("NEXMO_NUMBER")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class ConnectHandler(tornado.web.RequestHandler):
    def get(self):
        conversation_uuid = self.get_arguments("conversation_uuid")[0]
        print("conversation_uuid", conversation_uuid)
        ncco = [
            {
               "action": "connect",
               "from": NEXMO_NUMBER,
               "endpoint": [
                   {
                      "type": "websocket",
                      "uri" : "ws://"+HOSTNAME+"/socket",
                      "content-type": "audio/l16;rate=16000",
                      "headers": {
                        "conversation_uuid":conversation_uuid
                      }
                   }
               ]
             }
        ]
        print(ncco)
        self.write(json.dumps(ncco))
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ncco", ConnectHandler),

    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8001)
    tornado.ioloop.IOLoop.current().start()
