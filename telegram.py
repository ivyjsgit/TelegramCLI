from telethon import TelegramClient, events, sync
# import telethon.tl.types.PeerChannel
from PyQt5.QtWidgets import QApplication, QLabel

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 
api_hash = ''


def print_messages(numChats):
    count = 0
    ids = []
    entities = []
    for dialog in client.get_dialogs(limit = numChats):
        message = dialog.message
       
        if(message.from_id is None):
            peer_id = message.to_id.channel_id
            entity = message.to_id
            print('(' + str(count) + ') ' + dialog.name + ": " + message.message)
        else:
            userID = message.from_id
            try:
                entity = message.from_id
                peer_id = message.to_id.user_id
                print("We got a single message!")
                # print(message.stringify())
            except:
                print("We got a group!")
                # print(message.stringify())
                entity = message.to_id
                peer_id = message.to_id.channel_id
            userName = getUsername(userID)
            print('(' + str(count) + ') ' + dialog.name + ' - ' + userName + ": " + message.message)
        ids.append(str(peer_id))
        entities.append(entity)
        # print(message.stringify())
        count +=1
    # print(ids)
    # print(entities)
    select_username(ids, entities)
    
def select_username(ids, entities):
    userInput = input("Selection: ")
    print("Loading selection: " + ids[int(userInput)])
    loadChat(entities[int(userInput)])

def loadChat(entity):
    # messages = client.iter_messages(id)
    messages = client.get_messages(entity, limit = 10)
    messages.reverse()
    for message in messages:
        printTextualMessage(message)
    chatOptions(entity)
def chatOptions(entity):
    option = input("Options- (S)end : ")
    if(option.lower == "s"):
        sendMessage(entity)
def sendMessage(entity):
    message = input("Message: ")
    client.send_message(entity, message=message)

def printTextualMessage(message):
    username = getUsername(message.from_id)
    message = message.message
    print(username + ": " + message)


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
# print(client.get_me().username)


# app = QApplication([])
# label = QLabel(username + " - " + userID)
# label.show()
# app.exec_()

