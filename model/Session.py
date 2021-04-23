from model import Message
from helper import MessageParser
import socket


class Session:

    def __init__(self):
        self.socket_list = []

    def broadcast_message(self, msg: bytearray, s: socket.socket):
        for c_socket in self.socketList:
            if c_socket != s:
                c_socket.sendall(msg)
                log: Message.Message = MessageParser.byte_array_to_message(msg)
