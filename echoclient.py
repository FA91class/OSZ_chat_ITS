import socket
from model import Message
from helper import Style
from datetime import datetime
from helper import MessageParser
from helper import const
import threading

HOST = const.HOST
PORT = const.PORT

def mlisten(s: socket):
    while True:
        data = s.recv(1024)
        if not data:
            break
        m = MessageParser.bytearraytomessage(data)
        print(Style.printmessage(m))

print("Welcome to ChatZ")

UNAME = input("Whats your name? :")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    threading.Thread(target=mlisten, args=(s))
    while True:
        string = input("New Message: ")
        if "!logout" in string:
            break
        m = Message.Message(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), string, UNAME)
        send = MessageParser.messagetobytearray(m)

        s.send(send)
