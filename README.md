# AnsweringMachineDetection

*Try it Out*
Dial: +1(201)582-2833

To install:
` pip install -r requirements.txt`

Create a .env file with the following
```
HOSTNAME={SERVER_URL}
NEXMO_NUMBER={YOUR NEXMO NUMBER}
NEXMO_APP_ID={NEXMO APP ID}
CONF_NAME={NAME OF CONFERENCE} which can be anything
```
to Run:
run:`python websocket-demo.py`
the Application will ask for a number to dial. You can enter in your own cell phone number
You'll then recieve a call from that Nexmo Number
Do not answer the call, just send to voicemail
You will then here the voicemail from your phone
When the beep is detected, you will here the following response
`We have detected your answering machine. Thats ok, we\'ll call you back later`
The call will then hangup


To run as a standalone application, you can connect to the websocket, and the use a seperate websocket client to listen to events:
For your purchased Nexmo number, set your Answer NCCO to:
```
[
            {
               "action": "connect",
               "from": {NEXMO_NUMBER},
               "endpoint": [
                   {
                      "type": "websocket",
                      "uri" : "ws://careangel-amd-detector.herokuapp.com/socket",
                      "content-type": "audio/l16;rate=16000",
                      "headers": {
                      }
                   }
               ]
             }
        ]
```
This will only send the audio data to the websocket.
In order to get events, you will need to create a client to connect to the websocket

```NodeJS
const WebSocket = require('ws');

const ws = new WebSocket('ws://careangel-amd-detector.herokuapp.com/socket');
ws.on('message', function incoming(data) {

//messages will be returned here
  console.log(data);
});
```

Once the call is connected to the websocket, you will send the following logs to the nodeJS application
{"beep_detected": false}
Once a beep is detected, you will see
{"beep_detected": true}
