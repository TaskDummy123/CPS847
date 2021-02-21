import slack
import os
from pathlib import Path
from dotenv import load_dotenv
# Import Flask
from flask import Flask, request, Response
# Handles events from Slack
from slackeventsapi import SlackEventAdapter
# Used for sending requests to OpenWeather API
import requests
# Import a custom class for the bot's weather message
from WeatherMessage import WeatherMessage

# Load the Token from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Configure your flask application
app = Flask(__name__)

# Configure SlackEventAdapter to handle events
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

# Using WebClient in slack, there are other clients built-in as well !!
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

# connect the bot to the channel in Slack Channel
client.chat_postMessage(channel='#general', text='Send Message Demo')

# Get Bot ID
BOT_ID = client.api_call("auth.test")['user_id']


# handling Message Events
@slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    # this get the user text
    text2 = event.get('text')
    if BOT_ID !=user_id:
        # send message
        # if question echo it
        if(text2[-1] == '?'):
            client.chat_postMessage(channel=channel_id, text=text2)

# handling Weather Command
@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.form
    params = data.get('text').split()
    channel_id = data.get('channel_id')

    if params and params[0]:
        # OpenWeather API call for city input
        param_city = '+'.join(params).strip().lower()
        weather_res = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(param_city, os.environ['OPEN_WEATHER_KEY']))

        if weather_res.status_code == 200:
            # As the bot, obtain the OpenWeather API response and send a new message to the channel, displaying the queried information
            weather_query = weather_res.json()
            resp_obj = WeatherMessage(weather_query)
            resp_blocks = resp_obj.get_message_blocks()
            client.chat_postMessage(channel=channel_id, username='Welcome Robot!', icon_emoji=':robot_face:', blocks=resp_blocks)

            # OK : OpenWeather API call was successful and bot is expected to send a new message to the channel
            return Response(), 200
        # Service Unavailable : OpenWeather API will not accept a request at this time
        return Response(), 503
    # Bad Request : invalid syntax; the /weather command must have at least 1 parameter
    return Response(), 400

# Run the webserver micro-service
if __name__ == "__main__":
    app.run(debug=True)
