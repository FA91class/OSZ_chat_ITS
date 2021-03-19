from model import Message
from helper import MessageParser
import socket


class Session:

    def __init__(self):
        self.socketList = []

    def broadcast_message(self, msg: bytearray, s: socket.socket):
        for cSocket in self.socketList:
            if cSocket != s:
                cSocket.sendall(msg)
                log: Message.Message = MessageParser.byte_array_to_message(msg)
