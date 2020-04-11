from slacker import Slacker
# pip install slacker

from config import slackAPItoken
# OR
# slackAPItoken = "YOUR-LEGACY-API-TOKEN-HERE"


# Authenticate with slacker
slack = Slacker(slackAPItoken)

if slack.api.test().successful:
    print(
        f"Connected to {slack.team.info().body['team']['name']}.\n")
else:
    print('Try Again!')
    exit()


# Make a request to get the channels
r = slack.conversations.list(types="public_channel, private_channel", exclude_archived=True)
channels = r.body

# Iterate through channels
for i, c in enumerate(channels['channels']):
    print(f'{i}. Channel {c["name"]} ')
    # print(f'Channel {c["name"]} ID {c["id"]} Purpose: {c["purpose"]["value"]}')
print("")

# FROM
ch = int(input("Select **FROM** channel from list: "))
fromChannel = channels['channels'][ch]
print("You selected channel {}\n".format(fromChannel['name'] ))

# TO
ch = int(input("Select **TO** channel from list: "))
toChannel = channels['channels'][ch]
print("You selected channel {}\n".format(toChannel['name'] ))

# hardcoded for testing purpose, comment this to use **TO** toChannel instead 
toChannel['id'] = "G010XT1138X"

# Make a request to get conversation history
r = slack.conversations.history(fromChannel['id'])
conversations = r.body


sender_name = input("Include sender name in forward message? (Y/N): ")
yes = ['Y', 'y', 'yes', 'Yes']
success = []

# loop thorugh all msgs and send them one-by-one
for msg in conversations["messages"][::-1]:
    if (sender_name in yes ):
        user = "<@" +msg['user'] + ">: "
    else:
        user = ""
    
    # exclude group join msgs
    if('subtype' in msg and msg['subtype']=='group_join'):
        continue


    if "attachments" in msg:
        r = slack.chat.post_message(channel=toChannel['id'], text=user + msg['text'], attachments= msg['attachments'])
    elif "files" in msg:
        continue
    else:
        r = slack.chat.post_message(channel=toChannel['id'], text=user + msg['text'])

    response = r.body
    success.append(response['ok'])

print("")
print("{} messages succesfully forwarded".format(success.count(True)))
print("{} messages failed while forwarding".format(success.count(False)))
