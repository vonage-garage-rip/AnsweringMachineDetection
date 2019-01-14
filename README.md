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

