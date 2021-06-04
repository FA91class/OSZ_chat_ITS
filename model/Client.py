from socket import socket
import uuid


class Client(object):
    def __init__(self, cSocket: socket, cid: str):
        super(Client, self).__init__()

        self.id: str = cid
        self.cSocket: socket = cSocket
        self.trueId: str = str(uuid.uuid4())
