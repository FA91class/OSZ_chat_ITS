from model import Message
from helper import MessageParser
from typing import List
import socket


class Session:

    socket_list: List[socket.socket]

    def __init__(self):
        self.socket_list = []

    def broadcast_message(self, msg: bytearray, s: socket.socket):
        for c_socket in self.socket_list:
            if c_socket != s:
                c_socket.sendall(msg)
                log: Message.Message = MessageParser.byte_array_to_message(msg)
