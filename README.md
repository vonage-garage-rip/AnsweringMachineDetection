# AnsweringMachineDetection

For this solution, we built a machine learning algorithm that is able to detect when a call goes to voicemail by listening to the `beep` sound with 96% accuracy. When the call is picked up by the answering machine, we perform a speech-to-text action(TTS) which is recorded by the answering machine.

## Try it out on Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://nexmo.dev/answering-machine-detection-install)

After you deploy the application to Heroku, make a call to the purchased number for the application.

The application will ask to enter a phone number. 
Enter any phone number you like, as long as it is picked up by voicemail. The call will go to voicemail and the answering machine model will start listenting on the call.

When a beep is detected, the application performs a Text-To-Speech, with the phrase, `Answering Machine Detected`, and the call will hangup.

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
