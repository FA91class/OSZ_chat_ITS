from typing import List

from helper import const
from helper.ApiCaller import APICaller
from model.Client import Client


class Session:
    client_list: List[Client]

    def __init__(self):
        self.client_list = []

    def broadcast_message(self, msg: bytearray, client: Client):
        for client_i in self.client_list:
            try:
                response: bytes = APICaller.encryptData(msg, const.SERVER_MODE, client_i.id)
                client_i.cSocket.sendall(response)

            except (ConnectionAbortedError, ConnectionResetError):
                self.client_list.remove(client)
                client.cSocket.close()
