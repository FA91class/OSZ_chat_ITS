import socket
import sys
import threading
from datetime import datetime

from helper import MessageParser
from helper import const
from model import Message

HOST = const.HOST
PORT = const.PORT
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def message_listener(s: socket):
    try:
        while True:
            data = s.recv(1024)
            if not data:
                break
            m: Message.Message = MessageParser.byte_array_to_message(data)
            print(m.msg)
    except (ConnectionAbortedError, ConnectionResetError):
        print("Connection with server closed!")


print("Welcome to ChatZ")

UNAME = input("Whats your name? :")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        thread = threading.Thread(target=message_listener, args=[s])
        thread.start()
        m = Message.Message(datetime.now().strftime(const.TIME_FILTER), "LOGIN", UNAME)
        send = MessageParser.message_to_byte_array(m)
        s.send(send)
        while True:
            string = input("$~ ")
            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(ERASE_LINE)
            if "!logout" in string:
                m = Message.Message(datetime.now().strftime(const.TIME_FILTER), "LOGOUT", UNAME)
                send = MessageParser.message_to_byte_array(m)

                s.send(send)
                break
            m = Message.Message(datetime.now().strftime(const.TIME_FILTER), string, UNAME)
            send = MessageParser.message_to_byte_array(m)

            s.send(send)

except (ConnectionAbortedError, ConnectionResetError):
    print("Connection with server closed!")
