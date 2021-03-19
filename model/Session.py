from model import Message
import socket


class Session:

    def __init__(self):
        self.socketList = []

    def broadcast_message(self, msg: Message.Message, s: socket.socket):
        for cSocket in self.socketList:
            if cSocket != s:
                cSocket.sendall(msg)
