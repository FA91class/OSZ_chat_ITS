import socket
from helper import MessageParser
from helper import Style
from helper import const
import threading

HOST = const.HOST
PORT = const.PORT

def on_new_client(clientsocket:socket.socket, addr, globalsocket:socket.socket):
    print('Connected by', addr)
    while True:
        msg = clientsocket.recv(1024)
        if not msg:
            break
        m = MessageParser.bytearraytomessage(msg)
        print(Style.printmessage(m))
        globalsocket.sendall(msg)
    clientsocket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        threading.Thread(target=on_new_client, args=(conn, addr, s))
