from model import Message


def space():
    print("")
    print("-------------------------------------------------------------")
    print("")


def print_message(msg: Message.Message):
    print("[" + msg.timestamp + "](" + msg.sender + "): " + msg.msg)


def logout_message(msg: Message.Message):
    print("[" + msg.timestamp + "](" + msg.sender + ") // Logged out ")


def login_message(msg: Message.Message):
    print("[" + msg.timestamp + "](" + msg.sender + ") // Logged out ")
