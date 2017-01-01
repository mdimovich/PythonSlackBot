# Python Slack Bot: Michael Dimovich 
import os
import time
from slackclient import SlackClient


BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# Handle the various commands 
# Figure out a way to do arithmetic operations and send back to slack channel
def handle_command(command, channel):
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    slack_client.api_call("chat.postMessage", channel="#botpractice",
                          text=response, as_user=True)
    if command.find("add") != -1:
        slack_client.api_call("chat.postMessage", channel="#botpractice", text="What would you like to add?", as_user=True)
    if command == "do list users":
        slack_client.api_call("chat.postMessage", channel="#botpractice", text="Users are...Unknown " , as_user=True)

# Return formatted text after messaging bot
def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None


READ_WEBSOCKET_DELAY = 1
if slack_client.rtm_connect():
    print("StarterBot connected and running")
    # Practice call to verify channel connection
    slack_client.api_call("chat.postMessage", channel="#botpractice", text="Bot up and running")
    while True:
        command, channel = parse_slack_output(slack_client.rtm_read())
        if command and channel:
            handle_command(command, channel)
        time.sleep(READ_WEBSOCKET_DELAY)
else:
    print("Connection failed. Problem with token or ID")
