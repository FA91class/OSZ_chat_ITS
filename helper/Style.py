from model import Message


def space():
    print("")
    print("-------------------------------------------------------------")
    print("")


def print_message(msg: Message.Message):
    message = "[" + msg.timestamp + "](" + msg.sender + "): " + msg.msg
    print(message)
    return message


def logout_message(msg: Message.Message):
    return "[" + msg.timestamp + "](" + msg.sender + ") // Logged out "


def login_message(msg: Message.Message):
    return "[" + msg.timestamp + "](" + msg.sender + ") // Logged in "
