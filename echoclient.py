import socket
import sys
import threading
from datetime import datetime

from helper import MessageParser
from helper import const
from helper.ApiCaller import APICaller
from model.Message import Message

HOST = const.HOST
PORT = const.PORT
CURSOR_UP_ONE = '\033[A'
ERASE_LINE = '\033[2K'


def message_listener(skt: socket.socket):
    try:
        while True:
            data = skt.recv(1024)
            if not data:
                break
            msg: Message = MessageParser.bytes_to_message(
                APICaller.decryptData(data, const.CLIENT_MODE))
            print(msg.msg)
    except (ConnectionAbortedError, ConnectionResetError):
        print("Connection with server closed!")


print("Welcome to ChatZ")

UNAME = input("Whats your name? :")
APICaller.createNewKey(UNAME.strip(), const.CLIENT_MODE)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        thread = threading.Thread(target=message_listener, args=[s])
        thread.start()
        m = Message(datetime.now().strftime(
            const.TIME_FILTER), "LOGIN", UNAME)
        send = MessageParser.message_to_bytes(m)
        s.send(APICaller.encryptData(send, const.CLIENT_MODE, m.sender))
        while True:
            string = input("")
            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(ERASE_LINE)
            if "!logout" in string:
                m = Message(datetime.now().strftime(
                    const.TIME_FILTER), "LOGOUT", UNAME)
                send = MessageParser.message_to_bytes(m)

                s.send(APICaller.encryptData(
                    send, const.CLIENT_MODE, m.sender))
                break
            m = Message(datetime.now().strftime(
                const.TIME_FILTER), string, UNAME)
            send = MessageParser.message_to_bytes(m)

            s.send(APICaller.encryptData(send, const.CLIENT_MODE, m.sender))

except (ConnectionAbortedError, ConnectionResetError):
    print("Connection with server closed!")
