from helper.ApiCaller import APICaller
from model.Client import Client
from model.Message import Message
from helper import MessageParser
from helper import Logger
from helper import const
from typing import List
import socket


class Session:

    socket_list: List[Client]

    def __init__(self):
        self.socket_list = []

    def broadcast_message(self, msg: bytearray, client: Client):
        for c_socket in self.socket_list:
            if c_socket.id != client: 
                response: bytes = APICaller.encryptData(msg, const.SERVER_MODE, client.id)
                c_socket.sckt.sendall(response)
