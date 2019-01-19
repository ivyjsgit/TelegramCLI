from telethon import TelegramClient, events, sync, types
# import telethon.tl.types.PeerChannel
from PyQt5.QtWidgets import QApplication, QLabel
import os

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 
api_hash = ''


def print_messages(numChats):
#This method lists the latest chats up to a certain number
    ourID = client.get_me().id
    # print(ourID)
    # ourID = 
    count = 0
    ids = []
    entities = []
    for dialog in client.get_dialogs(limit = numChats):
        message = dialog.message
        entity = dialog.entity
        # print(dialog.entity.stringify())
        if(message.from_id is None):
            print("Message is from a channel!")
            peer_id = message.to_id.channel_id
            entity = message.to_id
            print('(' + str(count) + ') ' + dialog.name + ": " + message.message)
        else:
            from_id = message.from_id
            message_sender_username = getUsername(from_id)
            if(message.action is None):
                print('(' + str(count) + ') ' + dialog.name + "- " + message_sender_username + ": "+ message.message)
            elif(type(message.action) is types.MessageActionChatJoinedByLink):
                print('(' + str(count) + ') ' + dialog.name + "- " + message_sender_username + " joined the group")

        # ids.append(str(peer_id))
        entities.append(entity)
        count +=1
    select_username(entities)
    
def select_username(entities):
    userInput = input("Selection: ")
    loadChat(entities[int(userInput)])

def loadChat(entity):
    print(entity)
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        print(entity.title)
    except:
        try:
            print(getUsername(entity.id))
        except:
            pass

    messages = client.get_messages(entity, limit = 10)
    messages.reverse()
    for message in messages:
        printTextualMessage(message)
        # print(message)
    chatOptions(entity)
def chatOptions(entity):
    option = input("Options- (S)end (R)efresh (C)hats: ")
    print(option)
    if option.lower() == 's' :
        # print("Sending!!!")
        sendMessage(entity)
    if option.lower() == 'r':
        loadChat(entity)
    if option.lower() == 'c':
        os.system('cls' if os.name == 'nt' else 'clear')
        print_messages(10)
    else:
        sendMessage(entity, option)

def sendMessage(entity):
    message = input("Message: ")
    client.send_message(entity, message=message)
    loadChat(entity)
    chatOptions(entity)
def sendMessage(entity, message):
    client.send_message(entity, message=message)
    loadChat(entity)
    chatOptions(entity)

def printTextualMessage(message):
    # print(message)
    try:
        username = getUsername(message.from_id)
        # print(message.action)
        if(type(message.action) is types.MessageActionChatJoinedByLink):
            print(username + " joined the group")
        else:
            message = message.message
            print(username + ": " + message)
    except:
        if(message.action is types.MessageActionChatJoinedByLink):
            print("Woah!")
        # print(message)
        print("Uhh")

def getUsername(userID):
    user = client.get_entity(userID)
    firstName = user.first_name
    if(user.last_name == None):
        return firstName
    else:
        last_name = user.last_name
    return firstName + " " +last_name
client = TelegramClient('session_name', api_id, api_hash)
client.start()
username = client.get_me().username
userID = str(client.get_me().id)
print("Signed in as " + username + " - " + userID)
print_messages(10)
