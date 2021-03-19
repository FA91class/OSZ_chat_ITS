from model import Message


class Session:

    def __init__(self):
        self.socketList = []

    def broadcast_message(self, msg: Message.Message):
        for cSocket in self.socketList:
            cSocket.sendall(msg)
