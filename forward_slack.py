from slacker import Slacker
from config import slackAPItoken


# Authenticate with slacker
# get from Slack legacy API
slack = Slacker(slackAPItoken)

if slack.api.test().successful:
    print(
        f"Connected to {slack.team.info().body['team']['name']}.")
else:
    print('Try Again!')


# Make a request to get the channels
r = slack.conversations.list(types="public_channel, private_channel", exclude_archived=True)
channels = r.body

# Iterate through channels
for i, c in enumerate(channels['channels']):
    print(f'{i}. Channel {c["name"]} ')
    # print(f'Channel {c["name"]} ID {c["id"]} Purpose: {c["purpose"]["value"]}')



ch = int(input("\nSelect channel from list: "))
fromChannel = channels['channels'][ch]['id']

# hardcoded for testing purpose
toChannel = "G010XT1138X"

# Make a request to get conversation history
r = slack.conversations.history(fromChannel)
conversations = r.body

# Iterate through conversation body
for msg in conversations["messages"]:
    if "attachments" in msg:
        r = slack.chat.post_message(channel=toChannel, text=msg['text'], attachments= msg['attachments'])
    elif "files" in msg:
        continue
        # r = slack.chat.post_message(channel="G010XT1138X", text=msg['text'], attachments= msg['files'])
    else:
        r = slack.chat.post_message(channel="G010XT1138X", text=msg['text'])

    # response = r.body
    # print(response['ok'])
