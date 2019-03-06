# AnsweringMachineDetection

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://nexmo.dev/answering-machine-detection-install)

For this solution, we built a machine learning algorithm that is able to detect when a call goes to voicemail by listening to the `beep` sound with 96% accuracy. When the call is picked up by the answering machine, we perform a text-to-speech action(TTS) which is then recorded by the answering machine.

## Running the app

### Using Docker

To run the app using Docker run the following command in your terminal:

```bash
docker-compose up
```

This will create a new image with all the dependencies and run it at `http://localhost:8000`.

You can declare the required environment variables by editing the `docker-compose.yml` file.

### Local Install

To run this on your machine you'll need an [up-to-date version of Python 3](https://www.python.org/downloads/).

Clone the [github repo](https://github.com/nexmo-community/AnsweringMachineDetection) and run: 

`pip install -r requirements.txt`

Create a `.env` file with the following
```python
MY_LVN={YOUR_NEXMO_NUMBER}
APP_ID={YOUR_NEXMO_APPLICATION_ID}
PRIVATE_KEY={PATH_TO_APPLICATION_PRIVATE_KEY}
```
By default the server runs on port 8000.

Tools like [ngrok](https://ngrok.com/) are great for exposing ports on your local machine to the internet. If you haven't done this before, [check out this guide](https://www.nexmo.com/blog/2017/07/04/local-development-nexmo-ngrok-tunnel-dr/).

## Running the example

If you are working with a local install you can run the server using this command:

```bash
python websocket-demo.py
```

## Linking the app to Nexmo

You will need to create a new Nexmo application in order to work with this app:

### Create a Nexmo Application Using the Command Line Interface

Install the CLI by following [these instructions](https://github.com/Nexmo/nexmo-cli#installation). Then create a new Nexmo application that also sets up your `answer_url` and `event_url` for the app running locally on your machine.

```bash
nexmo app:create answering-machine-detection http://<your_hostname>/ncco http://<your_hostname>/event
```

This will return an application ID. Make a note of it.

### Rent a New Virtual Number

If you don't have a number already in place, you will need to rent one. This can also be achieved using the CLI by running this command:

```bash
nexmo number:buy
```

### Link the Virtual Number to the Application

Finally, link your new number to the application you created by running:

```bash
nexmo link:app YOUR_NUMBER YOUR_APPLICATION_ID
```

## Try it out

With your application running, make a call to the purchased number.

The application will ask to you to enter a phone number. 
Enter any phone number you like, as long as it is picked up by voicemail. The call will go to voicemail and the answering machine model will start listenting on the call.

When a beep is detected, the application performs a Text-To-Speech, with the phrase, `Answering Machine Detected`, and the call will hangup.
