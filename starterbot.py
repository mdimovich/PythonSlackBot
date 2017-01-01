import os
import time
from slackclient import SlackClient
import json


# Note: The BOT_ID has to be an environment variable for this to work
BOT_ID = os.environ.get("BOT_ID")


AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# Grabs Authentication Token. Needs to be an environment variable.
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Processing Command..."
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
    # Function for adding. Not sure how to implement yet.
    if command == "do add":
        slack_client.api_call("chat.postMessage", channel=channel, text="What would you like to add? :tada:", as_user=True)
        if command == "5+4":
            slack_client.api_call("chat.postMessage", channel=channel, text="The sum is: " + str(5+4))
    if command == "do list users":
        users = slack_client.api_call("users.list")
        userList = []
        if users.get('ok'):
            members = users.get('members')
            for user in range(0, len(members)):
                slack_client.api_call("chat.postMessage", channel=channel, text=members[user].get('name'))
                userList.append(members[user].get('name'))
                print (userList)
    if command == "do list names":
        users = slack_client.api_call("users.list")
        nameList = []
        if users.get('ok'):
            members = users.get('members')
            for user in range(0, len(members)):
                slack_client.api_call("chat.postMessage", channel=channel, text=members[user].get('real_name'))
                nameList.append(members[user].get('real_name'))
                print(nameList)
       # print(parsed_users)
       # slack_client.api_call("chat.postMessage", channel=channel, text="Some text testing 1,2")
    # Sends a thumbs up emoji message
    if command == "do thumbs up":
        slack_client.api_call("reactions.add", channel=channel, name="thumbsup", timestamp="1234567890.123456")
        slack_client.api_call("chat.postMessage", channel=channel, text=":thumbsup:", as_user=True)
    if command == "do list channels":
        slack_client.api_call("channel.list")
    # For uploading files, but doesn't work yet
    if command == "do upload file":
        slack_client.api_call("files.upload", filename="file.txt", file="multipart/form-data", channel=channel)
    # Test function that tests all of the different postMessage capabilities.
    # Note: Attachments is in JSON format
    if command == "do test":
        slack_client.api_call("chat.postMessage",icon_emoji=":smile:", channel=channel, attachments=[{"pretext": "Hey there","title": "Testing Section", "color": "good", "text": "This is the text"}])

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None


READ_WEBSOCKET_DELAY = 1
if slack_client.rtm_connect():
    print("StarterBot up and running!")
    # Test Message to make sure bot can post to channel #botpractice
    slack_client.api_call("chat.postMessage", channel="#botpractice", text="Bot up and running")
    while True:
        command, channel = parse_slack_output(slack_client.rtm_read())
        if command and channel:
            handle_command(command, channel)
        time.sleep(READ_WEBSOCKET_DELAY)
else:
    print("Connection failed. Problem with token or ID")
