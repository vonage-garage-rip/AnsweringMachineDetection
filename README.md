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
There are 2 python scripts that need to be run. 
The first, `python websocket-demo.py` is the websocket.
Running this script will start the server and detect whenever a answering machine is detected
The second script, 'websocket-client' is a script that connects to the websocket. 
This script will output the uuid of the current call as well as a value indicating if a beep was detected
```
{'uuid': '7d0fcfae6bb547fb6fed825f41c0cdf1', 'beep_detected': False}
````
run:`python websocket-demo.py`
the Application will ask for a number to dial. You can enter in your own cell phone number
You'll then recieve a call from that Nexmo Number
Do not answer the call, just send to voicemail
You will then here the voicemail from your phone
When a answering machine beep is detected, you will see the following when running `'websocket-client.py`
```
{'uuid': '7d0fcfae6bb547fb6fed825f41c0cdf1', 'beep_detected': True}
```
When `beep_detected` is `True`, the websocket-client will send a Text to Speech into the call
```
Answering Machine Detected
```


