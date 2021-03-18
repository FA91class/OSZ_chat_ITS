from model import Message

def space():
    print("")
    print("-------------------------------------------------------------")
    print("")

def printmessage(msg: Message.Message):
    print("[" + msg.timestamp +  "](" + msg.sender + "): " + msg.msg)

def logoutmessage(msg: Message.Message):
    print("[" + msg.timestamp + "](" + msg.sender + ") // Logged out ")

def logginmessage(msg: Message.Message):
    print("[" + msg.timestamp + "](" + msg.sender + ") // Logged out ")
