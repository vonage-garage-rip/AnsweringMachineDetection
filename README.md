# AnsweringMachineDetection

For this solution, we built a machine learning algorithm that is able to detect when a call goes to voicemail by listening to the `beep` sound with 96% accuracy. When the call is picked up by the answering machine, we perform a speech-to-text action(TTS) which is recorded by the answering machine.

## Try it out on Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

After you deploy the application to Heroku, make a call to the purchased number for the application.

The application will ask to enter a phone number. 
Enter any phone number you like, as long as it is picked up by voicemail.

To leave a TTS when the answering machine is picked up, run this python script, [websocket-client.py](websocket-client.py) locally.

Change the `HOSTNAME` property to heroku domain for the `{app-name}.herokuapp.com`

Note, you will need to install the Nexmo python package using:
`pip install nexmo`

When the voicemail is detected, you will see the following message in your console, when running the `websocket-client.py` script:

`{'uuids': ['xxx'], 'beep_detected': True}`

Then, the script plays a TTS saying `Answering Machine Detected`, and the call will hangup.

## To install
Clone the [github repo](https://github.com/nexmo-community/AnsweringMachineDetection) and run: 

`pip install -r requirements.txt`

Create a .env file with the following
```
MY_LVN={YOUR_NEXMO_NUMBER}
APP_ID={YOUR_NEXMO_APPLICATION_ID}
PRIVATE_KEY={PATH_TO_APPLICATION_PRIVATE_KEY}
```

You will need to create a [Nexmo Application](https://developer.nexmo.com/concepts/guides/applications) and [Purchase a phone number](https://developer.nexmo.com/numbers/building-blocks/buy-a-number)

There are 2 python scripts that need to be run. 
The first, `websocket-demo.py` is the websocket.
Running this script will start the server and detect whenever a answering machine is detected
