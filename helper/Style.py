from model import Message

def space():
    print("")
    print("-------------------------------------------------------------")
    print("")

def printmessage(msg: Message.Message):
    print("[" + msg.timestamp +  "](" + msg.sender + "): " + msg.msg)
