from socket import socket


class Client(object):
    def __init__(self, sckt, id):
        super(Client, self).__init__()
        
        self.id: str = id
        self.sckt: socket= sckt
