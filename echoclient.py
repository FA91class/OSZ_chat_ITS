import socket
from model import Message
from helper import Style
from datetime import datetime
from helper import MessageParser
from helper import const
import threading

HOST = const.HOST
PORT = const.PORT


def message_listener(s: socket):
    while True:
        data = s.recv(1024)
        if not data:
            break
        m = MessageParser.byte_array_to_message(data)
        print(Style.print_message(m))


print("Welcome to ChatZ")

UNAME = input("Whats your name? :")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    threading.Thread(target=message_listener, args=(s))
    while True:
        string = input()
        if "!logout" in string:
            break
        m = Message.Message(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), string, UNAME)
        send = MessageParser.message_to_byte_array(m)

        s.send(send)
